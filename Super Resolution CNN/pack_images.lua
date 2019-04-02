require('torch')
require('pl')
require('image')

local base_dir = '~/scrnn/data/'

local input_dir = base_dir .. 'inputs/'

local target_dir = base_dir .. 'targets/'

local input_set = nil

local target_set = nil

local length = 100

for i = 1, length do
	local num = i - 1
	local input_name = 'input_' .. num .. '.png'
	local target_name = 'tartget_' .. num .. '.png'
	local input_img_path = input_dir .. input_name
	local target_img_path = target_dir .. target_name
	local input_img = image.load(input_img_path, 3, 'byte')
	local target_img = image.load(target_img_path, 3, 'byte')

	local input_img_size_table = input_img:size():totable()
	local target_img_size_table = target_img:size():totable()
	table.insert(input_img_size_table, 1, 1)
	table.insert(target_img_size_table, 1, 1)
	local input_img_tensor = torch.reshape(input_img, unpack(input_img_size_table))
	local target_img_tensor = torch.reshape(target_img, unpack(target_img_size_table))
	if i == 1 then 
		input_set = input_img_tensor
		target_set = target_img_tensor
	else
		input_set = input_set:cat(input_img_tensor, 1)
		target_set = target_set:cat(target_img_tensor, 1)
	end
end

torch.save(base_dir .. 'inputs.t7', input_set)
torch.save(base_dir .. 'targets.t7', target_set)