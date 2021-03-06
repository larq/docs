## Are there any restrictions on using Larq?

We believe open research and software is the way forward for the field of Binarized Neural Network (BNN) and deep learning in general: machine learning can be a powerful engine for good, but only if it is transparent, safe and widely accessible. That is why we have made Larq open-source and free to use.

Larq is licensed under [Apache 2.0 licence](https://github.com/larq/larq/blob/master/LICENSE) - you are free to contribute to [Larq](https://github.com/larq/larq), fork it or build commercial applications on top of it. If you distribute a modified version of Larq, you should clearly state changes you have made and consider contributing them back.

## What is a Binarized Neural Network (BNN)?

A BNN is a deep neural network in which the bulk of the computations are performed using binary values. For example, in a convolutional layer we can use weights that are either -1 or 1, and similarly binarize the activations.

Binarization enables the creation of deep learning models that are extremely efficient: storing the model only requires a single bit per weight, and evaluating the model can be done very efficiently because of the bitwise nature of the operations.

Note that in BNNs not everything is binary: usually higher-precision computations are still used for things like the first layer, batch-normalization and residual connections.

## How can I cite Larq?

If Larq helps you in your work or research, it would be great if you can cite it as follows:

```bibtex
@article{larq,
  title     = {Larq: An Open-Source Library for Training Binarized Neural Networks},
  author    = {Lukas Geiger and Plumerai Team},
  year      = 2020,
  month     = jan,
  journal   = {Journal of Open Source Software},
  publisher = {The Open Journal},
  volume    = 5,
  number    = 45,
  pages     = 1746,
  doi       = {10.21105/joss.01746},
  url       = {https://doi.org/10.21105/joss.01746}
}
```

If your paper is publicly available, feel free to also add it to the list of papers using Larq below.

## What papers have used Larq?

One of the focuses of Larq is to accelerate research on neural networks with extremely low precision weights and activations.
Here is a list of papers that have used Larq:

* Helwegen et al. ["Latent weights do not exist: Rethinking binarized neural network optimization."](https://papers.nips.cc/paper/8971-latent-weights-do-not-exist-rethinking-binarized-neural-network-optimization.pdf) *Advances in Neural Information Processing Systems (NeurIPS)*. 2019.
    * Optimization of Binarized Neural Networks (BNNs) currently relies on real-valued latent weights to accumulate small update steps.
      In this paper, we argue that these latent weights cannot be treated analogously to weights in real-valued networks.
      Instead their main role is to provide inertia during training.
      We interpret current methods in terms of inertia and provide novel insights into the optimization of BNNs.
      We subsequently introduce the first optimizer specifically designed for BNNs, Binary Optimizer (Bop), and demonstrate its performance on CIFAR-10 and ImageNet.
      Together, the redefinition of latent weights as inertia and the introduction of Bop enable a better understanding of BNN optimization and open up the way for further improvements in training methodologies for BNNs.
    * Code available at: [plumerai/rethinking-bnn-optimization](https://github.com/plumerai/rethinking-bnn-optimization)
* Amir et al. ["An SMT-Based Approach for Verifying Binarized Neural Networks"](https://arxiv.org/abs/2011.02948). 2020.
    * Deep learning has emerged as an effective approach for creating modern software systems, with neural networks often surpassing hand-crafted systems.
    Unfortunately, neural networks are known to suffer from various safety and security issues.
    Formal verification is a promising avenue for tackling this difficulty, by formally certifying that networks are correct.
    We propose an SMT-based technique for verifying \emph{binarized neural networks} - a popular kind of neural networks, where some weights have been binarized in order to render the neural network more memory and energy efficient, and quicker to evaluate.
    One novelty of our technique is that it allows the verification of neural networks that include both binarized and non-binarized components.
    Neural network verification is computationally very difficult, and so we propose here various optimizations, integrated into our SMT procedure as deduction steps, as well as an approach for parallelizing verification queries.
    We implement our technique as an extension to the Marabou framework, and use it to evaluate the approach on popular binarized neural network architectures.

Have you used Larq for a paper? Feel free to make a pull request to add it to this list!

## Can I add my algorithm or model to Larq?

Absolutely! If you have developed a new model or training method that you would like to share with the community, create a PR or get in touch with us. Make sure you check out the contribution guide. For entire models with pretrained weights [`larq-zoo`](https://github.com/larq/zoo) is the correct place, everything else can be added to [`larq`](https://github.com/larq/larq) directly.

## Can I use Larq only for Binarized Neural Networks?

No, Larq is not just for BNNs! The real goal of Larq is to make it easy to work with extremely quantized networks. This includes BNNs as well as ternary networks (see for example [Ternary Weight Networks](https://arxiv.org/abs/1605.04711) or [Trained Ternary Quantization](https://arxiv.org/abs/1612.01064)). Although the focus is currently on BNNs, Larq already supports a [ternary quantizer](/larq/api/quantizers/#stetern) and binary and ternary networks have a lot in common. Moreover, modern BNNs are not 'pure' binary networks: they contain higher-precision first and last layers and shortcut connections, for example.

We will expand support for ternary and mixed-precision networks in the future by implementing layers and optimization tools that are useful in this context, and providing more examples. If there is any particular feature you would like to use, let us know by posting an [issue](https://github.com/larq/larq/issues).

## Why is Larq built on top of `tf.keras`?

We put a lot of thought into the question of which framework we should build Larq on and decided to go with TensorFlow / Keras over PyTorch or some other framework. There are a number of reasons for this:

- We really like the Keras API for its simplicity. At the same time, it is still very flexible if you want to build complex architectures or custom training loops.
- The TensorFlow ecosystem provides a wide range of tools for both researchers and developers. We think integration into that ecosystem will be beneficial for people working with BNNs.
- We are big fans of [`tf.datasets`](https://www.tensorflow.org/datasets/).
- Reproducibility is a key concern to us, and our approach for [`larq-zoo`](https://github.com/larq/zoo) is heavily inspired by [Keras Applications](https://keras.io/applications/).

## Will there be a `PyTorch` version of Larq?

No, currently we are not planning on releasing a `PyTorch` version of Larq.

## Can I use Larq for the deployment of my models?

Absolutely! For this purpose we have [Larq Compute Engine (LCE)](/compute-engine/): a highly optimized inference engine for deploying extremely quantized neural networks, such as Binarized Neural Networks (BNNs). LCE works seamlessly with the rest of Larq.
