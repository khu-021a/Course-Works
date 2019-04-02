require('torch')
require('nn')
require('nninit')
require('cunn')
require('cudnn')

local srcnn = torch.load('~/srcnn/out/out_model.t7')

local source_set = torch.load('~/testing/inputs/test_inputs.t7')

srcnn:cuda()

source_set = source_set:float():div(255):cuda()

local outs = srcnn:forward(source_set)

outs = outs:float():mul(255)

torch.save('/home/hk/srcnn/out/t0/t0_outs.t7', outs)