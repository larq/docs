# `larq.metrics`

We add metrics specific to extremely quantized networks using a `larq.context.metrics_scope` rather than through the `metrics` parameter of `model.compile()`, where most common metrics reside.
This is because, to calculate metrics like the `flip_ratio`, we need a layer's kernel or activation and not just the `y_true` and `y_pred` that Keras passes to metrics defined in the usual way.

{{autogenerated}}