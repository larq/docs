# `larq.constraints`

Functions from the `constraints` module allow setting constraints (eg. weight clipping) on network parameters during optimization.

The penalties are applied on a per-layer basis. The exact API will depend on the layer, but the layers `QuantDense`, `QuantConv1D`, `QuantConv2D` and `QuantConv3D` have a unified API.

These layers expose 2 keyword arguments:

- `kernel_constraint` for the main weights matrix
- `bias_constraint` for the bias.

```python
import larq as lq

lq.layers.QuantDense(64, kernel_constraint="weight_clip")
lq.layers.QuantDense(64, kernel_constraint=lq.constraints.WeightClip(2.0))
```

{{autogenerated}}
