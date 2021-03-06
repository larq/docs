# `larq.activations`

Activations can either be used through an `Activation` layer, or through the `activation` argument supported by all forward layers:

```python
import tensorflow as tf
import larq as lq

model.add(lq.layers.QuantDense(64))
model.add(tf.keras.layers.Activation('hard_tanh'))
```

This is equivalent to:

```python
model.add(lq.layers.QuantDense(64, activation='hard_tanh'))
```

You can also pass an element-wise TensorFlow function as an activation:

```python
model.add(lq.layers.QuantDense(64, activation=lq.activations.hard_tanh))
```

{{autogenerated}}
