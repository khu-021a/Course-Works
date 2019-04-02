local tnt = require('torchnet')
local argcheck = require('argcheck')

local hro_dataset = torch.class('hro_dataset', {})

hro_dataset.__init = argcheck{
  {name = 'self', type = 'hro_dataset'},
  {name = 'input_file', type = 'string'},
  {name = 'target_file', type = 'string'},
  call = function(self, input_file, target_file)
    local input_set = torch.load(input_file)
    local target_set = torch.load(target_file)
    self.inputs = input_set:float():div(255)
    self.targets = target_set:float():div(255)
  end
}

hro_dataset.iter = argcheck{
  {name = 'self', type = 'hro_dataset'},
  {name = 'batch_size', type = 'number', default = 32},
  {name = 'n_threads', type = 'number', default = 8},
  {name = 'train', type = 'boolean', default = 'true'},
  call = function(self, batch_size, n_threads, train)
    local inputs = self.inputs
    local targets = self.targets

    local function sample_by_index(index)
      return {
        input = inputs[index],
        target = targets[index]
      }
    end

    local indices = nil
    if train then
      local gen = torch.Generator()
      torch.manualSeed(gen, 19920226)
      indices = torch.randperm(gen, inputs:size(1)):long()
    else
      indices = torch.range(1, inputs:size(1)):long()
    end

    return tnt.ParallelDatasetIterator{
      ordered = true,
      nthread = n_threads,
      closure = function()
        local tnt = require('torchnet')

        return tnt.BatchDataset{
          batchsize = batch_size,
          dataset = tnt.ListDataset{
            list = indices,
            load = sample_by_index
          }
        }
      end
    }
  end
}

return hro_dataset