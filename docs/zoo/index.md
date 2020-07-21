# Larq Zoo Pretrained Models

Larq Zoo provides reference implementations of deep neural networks with extremely low precision weights and activations that are made available alongside pre-trained weights.
These models can be used for prediction, feature extraction, and fine-tuning.

The code for all models including a reproducible training pipeline is available at [`larq/zoo`](https://github.com/larq/zoo).

Larq Zoo consists of a `literature` and a `sota` submodule.

The [`literature`](/zoo/api/literature/) submodule contains replications from research papers (all current models).
These models are intended to provide a stable reference for ideas presented in specific papers.
The model implementations will be maintained, but we will not attempt to improve these models over time by applying new training strategies or architecture innovations.

The [`sota`](/zoo/api/sota/) submodule contains top models for various scenarios. These models are intended to be used in a [`SW 2.0`](https://medium.com/@karpathy/software-2-0-a64152b37c35)-like fashion.
We will do our best to continuously improve the models, which means that their weights and even details of their architectures may change from release to release.

If you have developed or reimplemented a Binarized or other Extremely Quantized Neural Network and want to share it with the community such that future papers can build on top of your work, please add it to Larq Zoo or [get in touch with us](https://spectrum.chat/larq/) if you need any help.

_Larq Zoo is part of a family of libraries for BNN development; you can also check out [Larq](https://docs.larq.dev/) for building and training BNNs and [Larq Compute Engine](/compute-engine/) for optimized deployment._

## Available models

The following models are trained on the [ImageNet](http://image-net.org/) dataset.
The Top-1 and Top-5 accuracy refers to the model's performance on the ImageNet validation dataset, memory refers to the memory after quantization of the weights.
Models were benchmarked using [Larq Compute Engine](/compute-engine/) on a [Pixel 1 phone (2016)](https://support.google.com/pixelphone/answer/7158570?hl=en-GB), single-threaded.

The model definitions and the train loops are available in the [Larq Zoo repository](https://github.com/larq/zoo).

The [`sota`](/zoo/api/sota/) submodule contains these models:

| Model                                         | Top-1 Accuracy | Top-5 Accuracy  | Model size | Latency (Pixel 1, single thread)[^1] |
| --------------------------------------------- | -------------- | --------------  | ---------- | ------------------------------------ |
| [QuickNet](/zoo/api/sota/#quicknet)           | 58.6 %         | 81.0 %          |  3.18 MB   | 18.4 ms                              |
| [QuickNetLarge](/zoo/api/sota/#quicknetlarge) | 62.7 %         | 84.0 %          |  4.49 MB   | 27.6 ms                              |
| [QuickNetXL](/zoo/api/sota/#quicknetxl)       | 67.0 %         | 87.3 %          |  6.22 MB   | 47.9 ms                              |

The [`literature`](/zoo/api/literature/) submodule contains the following models:

| Model                                                                   | Top-1 Accuracy | Top-5 Accuracy | Model size | Latency (Pixel 1, single thread)[^1] |
| ----------------------------------------------------------------------- | -------------- | -------------- | ---------- | ------------------------------------ |
| [RealToBinaryNet](/zoo/api/literature/#realtobinarynet)                 | 65.0 %         | 85.7 %         | 5.13 MB    | 51.3 ms                              |
| [BinaryDenseNet45](/zoo/api/literature/#binarydensenet45)               | 64.6 %         | 85.2 %         | 7.35 MB    | 138.5 ms                             |
| [BinaryDenseNet37Dilated](/zoo/api/literature/#binarydensenet37dilated) | 64.3 %         | 85.2 %         | 5.13 MB    | 182.9 ms                             |
| [BinaryDenseNet37](/zoo/api/literature/#binarydensenet37)               | 62.9 %         | 84.2 %         | 5.13 MB    | 102.2 ms                             |
| [MeliusNet22](/zoo/api/literature/#meliusnet22)                         | 62.4 %         | 83.9 %         | 3.88 MB    | 117.7 ms                             |
| [BinaryDenseNet28](/zoo/api/literature/#binarydensenet28)               | 60.9 %         | 82.8 %         | 4.04 MB    | 90.0 ms                              |
| [BinaryResNetE18](/zoo/api/literature/#binaryresnete18)                 | 58.3 %         | 80.8 %         | 4.00 MB    | 43.6 ms                              |
| [Bi-Real Net](/zoo/api/literature/#birealnet)                           | 57.5 %         | 79.8 %         | 4.00 MB    | 43.4 ms                              |
| [DoReFaNet](/zoo/api/literature/#dorefanet)                             | 53.4 %         | 76.5 %         | 22.80 MB   | Unsupported[^2]                      |
| [XNOR-Net](/zoo/api/literature/#xnornet)                                | 45.0 %         | 69.2 %         | 22.77 MB   | 34.9 ms                              |
| [Binary AlexNet](/zoo/api/literature/#binaryalexnet)                    | 36.3 %         | 61.5 %         | 7.45 MB    | 44.3 ms                              |

[^1]: Benchmarked on July 20st, 2020.
[^2]: DoReFaNet uses quantizers for which currently no optimized implemention is available in Larq Compute Engine.


## Installation

Larq Zoo is not included in Larq by default. To start using it, you can install it with Python's [pip](https://pip.pypa.io/en/stable/) package manager:

```shell
pip install larq-zoo
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
