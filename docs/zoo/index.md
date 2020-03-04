# Larq Zoo Pretrained Models

Larq Zoo provides reference implementations of deep neural networks with extremely low precision weights and activations that are made available alongside pre-trained weights.
These models can be used for prediction, feature extraction, and fine-tuning.

The code for all models including a reproducible training pipeline is available at [`larq/zoo`](https://github.com/larq/zoo).

Larq Zoo consists of a `literature` and a `sota` submodule.

The [`literature`](/zoo/api/literature/) submodule contains replications from research papers (all current models).
These models are intended to provide a stable reference for ideas presented in specific papers.
The model implementations will be maintained, but we will not attempt to improve these models over time by applying new training strategies or architecture innovations.

The [`sota`](/zoo/api/sota/) submodule contains top models for various scenarios. These models are intended to use in a [`SW 2.0`](https://medium.com/@karpathy/software-2-0-a64152b37c35)-like fashion.
We will do our best to continuously improve the models, which means that their weights and even details of their architectures may change from release to release.

If you have developed or reimplemented a Binarized or other Extremely Quantized Neural Network and want to share it with the community such that future papers can build on top of your work, please add it to Larq Zoo or get in touch with us if you need any help.

## Available models

The following models are trained on the [ImageNet](http://image-net.org/) dataset. The Top-1 and Top-5 accuracy refers to the model's performance on the ImageNet validation dataset, memory refers to the memory after quantization of the weights.

The model definitions and the train loop are available in the [Larq Zoo repository](https://github.com/larq/zoo).

The [`literature`](/zoo/api/literature/) submodule contains the following models:

| Model                                                                   | Top-1 Accuracy | Top-5 Accuracy | Parameters | Memory   |
| ----------------------------------------------------------------------- | -------------- | -------------- | ---------- | -------- |
| [BinaryDenseNet45](/zoo/api/literature/#binarydensenet45)               | 64.59 %        | 85.21 %        | 13 939 240 | 7.54 MB  |
| [BinaryDenseNet37Dilated](/zoo/api/literature/#binarydensenet37dilated) | 64.34 %        | 85.15 %        | 8 734 120  | 5.25 MB  |
| [BinaryDenseNet37](/zoo/api/literature/#binarydensenet37)               | 62.89 %        | 84.19 %        | 8 734 120  | 5.25 MB  |
| [BinaryDenseNet28](/zoo/api/literature/#binarydensenet28)               | 60.91 %        | 82.83 %        | 5 150 504  | 4.12 MB  |
| [BinaryResNetE18](/zoo/api/literature/#binaryresnete18)                 | 58.32 %        | 80.79 %        | 11 699 368 | 4.03 MB  |
| [Bi-Real Net](/zoo/api/literature/#birealnet)                           | 57.47 %        | 79.84 %        | 11 699 112 | 4.03 MB  |
| [DoReFaNet](/zoo/api/literature/#dorefanet)                             | 53.39 %        | 76.50 %        | 62 403 912 | 22.84 MB |
| [XNOR-Net](/zoo/api/literature/#xnornet)                                | 44.96 %        | 69.18 %        | 62 396 768 | 22.81 MB |
| [Binary AlexNet](/zoo/api/literature/#binaryalexnet)                    | 36.30 %        | 61.53 %        | 61 859 192 | 7.49 MB  |

The [`sota`](/zoo/api/sota/) submodule contains these models:

| Model                                         | Top-1 Accuracy | Top-5 Accuracy | Parameters | Memory  |
| --------------------------------------------- | -------------- | -------------- | ---------- | ------- |
| [QuickNet](/zoo/api/sota/#quicknet)           | 58.33 %        | 80.77 %        | 10 518 528 | 3.21 MB |
| [QuickNetLarge](/zoo/api/sota/#quicknetlarge) | 62.50 %        | 84.03 %        | 11 837 696 | 4.56 MB |

## Installation

Larq Zoo is not included in Larq by default. To start using it, you can install it with Python's [pip](https://pip.pypa.io/en/stable/) package manager:

```shell
pip install --pre larq-zoo
```

Weights can be downloaded automatically when instantiating a model. They are stored at `~/.larq/models/`.

## Training Models from Scratch

Larq Zoo ships with a command-line interface powered by [`zookeeper`](https://github.com/larq/zookeeper/), allowing you to reproduce the entire training process. If you want to improve an existing model or implement your own, we recommend to installing Larq Zoo in [development mode](https://github.com/larq/zoo/blob/master/CONTRIBUTING.md#project-setup).

E.g. to reproduce the training of [Binary AlexNet](/zoo/api/literature/#binaryalexnet) run:

```shell
lqz TrainBinaryAlexNet dataset=ImageNet
```

To experiment with different hyperparameters you can either edit the [task for this model](https://github.com/larq/zoo/blob/v1.0.b2/larq_zoo/experiments.py#L22) or overwrite them from the command line, e.g.:

```shell
lqz TrainBinaryAlexNet dataset=ImageNet epochs=100 batch_size=64
```

For all available commands and options run `lqz --help` or checkout the documentation of [`zookeeper`](https://github.com/larq/zookeeper/) if you want to implement your model for Larq Zoo.
