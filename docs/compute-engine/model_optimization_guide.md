# Optimizing models for Larq Compute Engine

Larq Compute Engine is capable of running any Larq model, but some model
architectures will perform better than others. These are some important
guidelines to follow when designing models to be run on LCE, so as to ensure
that inference is as fast as possible.

!!! important
    This guide assumes that you are deploying Larq Compute Engine on an Arm64
    device, such as an Android phone or a Raspberry Pi 4 board (with 64-bit OS).

*   **Use multiples of 32 input channels**

    The LCE binary ops (binary convolution and binary maxpool) operate on
    multiples of 32 input channels. Before a binary op, the input channels are
    padded out to a multiple of 32, which means that a binary convolution
    applied to an input with 16 channels and a binary convolution applied to an
    input with 32 channels will run equally fast.

*   **Use multiples of 8 output channels**

    The LCE optimised binary convolution op computes the result of 8 output
    channels in parallel, so if the number of output channels is not a multiple
    of 8 there will be wasted computation.

*   **Use `QuantConv2D` → `ReLU` → `BatchNormalization` to take advantage of op
    fusing**

    !!! warning
        This is not the convention used in TensorFlow Lite.

    Op fusing is an optimisation performed by the converter, whereby a
    sequence of stand-alone ops can be fused into an equivalent single op that
    can be executed more quickly than the original sequence.

    In the TensorFlow Lite converter, the layer sequence `Conv2D` →
    `BatchNormalization` → `ReLU` gets fused together into a single op. This
    makes sense, because the multiplier and addition of the batch-norm can be
    fused into the weights and bias of the convolution without any additional
    computation, and then the activation function can be applied at the end.

    However, in a binary convolution it is not possible to fuse the
    (full-precision) batch-norm multiplier into the (binary) convolution
    weights, and so there's no speed advantage to performing the batch-norm
    before the ReLU. Conversely, there *is* a possible advantage to performing
    the ReLU before the batch-norm for a sequence of binary convolutions: if the
    output of a ReLU were fed directly into a subsequent binary convolution, the
    input would be quantised to constant ones and all information would be
    destroyed. As a result, the LCE converter supports op fusing of the layer
    sequence `QuantConv2D` → `ReLU` → `BatchNormalization`.

    Note that a batch-norm can still be fused into a `QuantConv2D` layer without
    a ReLU between them; however, a subsequent ReLU would not also be fused.

*   **Avoid using Larq `QuantConv2D` layers with 'same-zero' padding**

    The [Keras `Conv2D`
    layer](https://www.tensorflow.org/api_docs/python/tf/keras/layers/Conv2D)
    supports either "valid" padding (no input padding) or "same" padding
    (padding the input with zeroes so that the output has the same spatial
    resolution). The Larq [`QuantConv2D`](/larq/api/layers/#quantconv2d) layer
    also supports "valid" and "same" padding, but additionally has an attribute
    `pad_values` that controls the padding constant that is used in the "same"
    padding case. We refer to the combination of `padding="same"` with
    `pad_values=0.0` (the default, to match the `Conv2D` layer) as 'same-zero'
    padding, and the combination with `pad_values=1.0` as 'same-one' padding.

    It is strongly recommended to use 'same-one' padding instead of 'same-zero'
    padding; for an example of models using 'same-one' padding, see the
    [QuickNet models in Larq
    Zoo](https://github.com/larq/zoo/blob/bb0dbf7c13bcb21149cd19c3bd51fe7d885b3bd8/larq_zoo/sota/quicknet.py#L107-L108).

    With 'same-zero' padding, because zero cannot be naturally represented in
    binary data (which uses a single bit to represent either +1 or -1) a
    zero-padding correction has to be added to values at the edge of the output
    tensor in order to give the correct result. This extra computation can be
    avoided by using 'same-one' padding.

    Additionally, 'same-zero' padding prevents the converter op fusing
    optimisations described above. These optimisations are not affected by
    'same-one' padding.

*   **Replace `QuantDense` layers with 1×1 `QuantConv2D`s**

    LCE does not yet include an optimised binary dense op, which means that Larq
    `QuantDense` layers are not accelerated in any way. The recommended
    workaround for this is to replace all `QuantDense` layers with an equivalent
    sequence of reshapes and a 1×1 `QuantConv2D` layer:

    ```python
    # Replace this...
    x = lq.layers.QuantDense(num_dense_outputs, ...)(x)

    # ...with this
    x = tf.keras.layers.Reshape((1, 1, -1))(x)
    x = lq.layers.QuantConv2D(num_dense_outputs, kernel_size=(1, 1), ...)(x)
    x = tf.keras.layers.Reshape((-1,))(x)
    ```

*   **Ensure that `filter_height` × `filter_width` × `input_channels` is a
    multiple of 128**

    Inside the optimised binary convolution op, an `im2col` procedure is applied
    to the input tensor, which reduces the convolution operation to a (binary)
    matrix multiplication. The `im2col`-transformed input has a depth of size
    `filter_height` × `filter_width` × `input_channels`, which is padded to a
    multiple of 128. If this value is already a multiple of 128, no padding is
    necessary, and so there is no unnecessary extra computation.
