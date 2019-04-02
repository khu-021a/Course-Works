[convergence]: images/convergence.png "Convergence Chart"

# Image Classification

This is the extensive implementation of [ResNet](https://arxiv.org/abs/1512.03385) with bottleneck layer.

## Prerequisites

* [Python](https://www.python.org/)
* [NumPy](http://www.numpy.org/)
* [Pillow](https://python-pillow.org/)
* [TensorFlow](https://www.tensorflow.org/)

## Model

**Main Architecture**

Layers | Layer Attributes | Input Size | Output Size
:---: | :---: | :---: | :---:
Conv + BN + ELU | K=3, S=2, P=1, F=64 | 254×254×3 | 128×128×64
Identity Block | | 128×128×64 | 128×128×64
Conv + BN + ELU | K=3, S=2, P=1, F=128 | 128×128×64 | 64×64×128
Identity Block | | 64×64×128 | 64×64×128
Conv + BN + ELU | K=3, S=2, P=1, F=256 | 64×64×128 | 32×32×256
Identity Block | | 32×32×256 | 32×32×256
Conv + BN + ELU | K=3, S=2, P=1, F=512 | 32×32×256 | 16×16×512
Identity Block | | 16×16×512 | 16×16×512
Conv + BN + ELU | K=3, S=2, P=1, F=1024 | 16×16×512 | 8×8×1024
Conv + BN + ELU | K=8, S=1, P=0, F=2048 | 8×8×1024 | 1×1×2048
Flatten | | 1×1×2048 | 2048
FC+Softmax | | 2048 | 48

**Identity Block Structure**

No. | Layers | Layer Attributes
:---: | :---: | :---: | :---:
1 | Conv + BN | K=1, S=1, P=1, F=f/2
2 | ELU |
3 | Conv + BN | K=1, S=1, P=1, F=f/2
4 | ELU |
5 | Conv + BN | K=1, S=1, P=1, F=f/2
6 | ELU |
7 | Conv + BN | K=1, S=1, P=1, F=f/2
8 | Add | Output of Layer 7 and Input Layer
9 | ELU |

*NOTE: K=kernel, S=stride, P=padding, F=filter number, f=initial filter number*

## Results

For parameters of the training process, the input images are in a 254-by-254 size with three channels, the batch size is 32 according to the input size, and the learning rate is 0.0002 to receive a feasible drop of the loss value. After training, a validation will be conducted to verify the performance of classification. There are totally 517651 pictures for the experiment, including 423598 of them for training and 94053 for validation.

The loss value is basically stabilized around 3.2 after six epochs but still fluctuates within a visible small range. The validation results are 60476 correct classifications out of total 94053 pictures, which indicates the accuracy is almost 64.3%.

**Convergence**
![Convergence][convergence]
