require('cudnn')
local nninit = require('nninit')

local model = {}

local Seq = nn.Sequential
local ReLU = cudnn.ReLU

local function Conv(...)
	local conv = cudnn.SpatialConvolution(...)
		:init('weight', nninit.normal, 0.0, 0.02)
		:init('bias', nninit.constant, 0)

  -- Use deterministic algorithms for convolution
	conv:setMode(
		'CUDNN_CONVOLUTION_FWD_ALGO_IMPLICIT_GEMM',
		'CUDNN_CONVOLUTION_BWD_DATA_ALGO_1',
		'CUDNN_CONVOLUTION_BWD_FILTER_ALGO_1')

	return conv
end

function model.srcnn()
	local net = Seq()
		:add(Conv(3, 64, 9,9, 1,1))
		:add(ReLU(true))
		:add(Conv(64, 32, 1,1, 1,1))
		:add(ReLU(true))
		:add(Conv(32, 3, 5,5, 1,1))
		:add(ReLU(true))
	
	return net
end

return model