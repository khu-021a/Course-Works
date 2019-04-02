require('torch')    -- Essential Torch utilities
require('image')    -- Torch image handling
require('nn')       -- Neural network building blocks
require('optim')    -- Optimisation algorithms
require('cutorch')  -- 'torch' on the GPU
require('cunn')     -- 'nn' on the GPU

local tnt = require('torchnet')
local pl = require('pl.import_into')()

--package.path = package.path .. ';./src/?.lua;./src/?/init.lua'
package.path = package.path .. ';./?.lua'

local hro_dataset = require('hro_dataset')
local model = require('model')


local n_epochs = 400
local n_batches_per_epoch = 128
local batch_size = 128
local learning_rate = 2e-5
local n_data_threads = 8
local train = true
local check_frequency = 10

torch.setdefaulttensortype('torch.FloatTensor')

local base_dir = '~/srcnn'
local data_dir = pl.path.join(base_dir, 'data')
local model_dir = pl.path.join(base_dir, 'model')

local input_path = pl.path.join(data_dir, 'train_inputs.t7')
local target_path = pl.path.join(data_dir, 'train_targets.t7')

local train_data = hro_dataset.new(input_path, target_path)
local train_iter = train_data:iter(batch_size, n_data_threads, train)


local srcnn_model = nil
local srcnn_path = pl.path.join(model_dir, 'srcnn.t7')

if pl.path.exists(srcnn_path) then
  print('Read models from files')
  srcnn_model = torch.load(srcnn_path)
else
  print('Create new models')
  srcnn_model = model.srcnn()
end

srcnn_model:cuda()

local srcnn_criterion = nn.MSECriterion()

srcnn_criterion:cuda()

local log_text = require('torchnet.log.view.text')

local log_keys = {'epoch', 'mse_loss', 'time'}

local log = tnt.Log{
  keys = log_keys,
  onFlush = {
    log_text{
      filename = 'srcnn_log.txt',
      keys = log_keys,
      format = {'epoch=%3d', 'mse_loss=%8.10f', 'time=%5.2fs'}
    }
  }
}

local srcnn_inputs = torch.CudaTensor(batch_size, 3, 33, 33)
local srcnn_targets = torch.CudaTensor(batch_size, 3, 21, 21)

local srcnn_params, srcnn_g_params = srcnn_model:getParameters()

local mse_loss_meter = tnt.AverageValueMeter()
local time_meter = tnt.TimeMeter()

local srcnn_backwards = function(new_params)
	if new_params ~= srcnn_params then
		srcnn_params:copy(new_params)
	end

	srcnn_g_params:zero()

	local outputs = srcnn_model:forward(srcnn_inputs)
	local loss = srcnn_criterion:forward(outputs, srcnn_targets)
	local dloss_doutputs = srcnn_criterion:backward(outputs, srcnn_targets)
	srcnn_model:backward(srcnn_inputs, dloss_doutputs)
	mse_loss_meter:add(loss)

	return loss, srcnn_g_params
end

local srcnn_optimiser = {
	method = optim.adam,
	config = {
		learningRate = learning_rate,
		beta1 = 0.5
	},
	state = {}
}

local instance_iter = train_iter()

for epoch = 1, n_epochs do
	print(os.date())
	print('In epoch ' .. epoch .. '...')

	mse_loss_meter:reset()
	time_meter:reset()

	for iteration = 1, n_batches_per_epoch do
		local sample = instance_iter()

		if not sample or sample.input:size(1) < batch_size or sample.target:size(1) < batch_size then
			-- Restart iterator
			iter_inst = train_iter()
			sample = iter_inst()
		end

		srcnn_inputs:copy(sample.input)
		srcnn_targets:copy(sample.target)

		srcnn_optimiser.method(
			srcnn_backwards,
			srcnn_params,
			srcnn_optimiser.config,
			srcnn_optimiser.state
		)
	end

	log:set{
		epoch = epoch,
		mse_loss = mse_loss_meter:value(),
		time = time_meter:value()
	}
	log:flush()

	if train then
		srcnn_model:clearState()
		torch.save(srcnn_path, srcnn_model)

		-- Checkpoint the networks every 5 epochs
		if epoch % check_frequency == 0 then
			pl.file.copy(srcnn_path, 
				pl.path.join(model_dir, string.format('srcnn_%04d.t7', epoch)))
		end
	end
end

print(os.date())
