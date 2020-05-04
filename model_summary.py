import tensorflow as tf
import larq_zoo as lqz
import larq as lq
import io
from functools import reduce


def html_format(source, language, css_class, options, md):
    model_fn = reduce(getattr, [lqz, *source.split(".")])
    stream = io.StringIO()
    tf.keras.backend.clear_session()
    lq.models.summary(model_fn(weights=None), print_fn=lambda s: print(s, file=stream))
    return f"""
    <details class="abstract"
      ><summary>Model Summary</summary>
      <pre class="model-summary"><code>{stream.getvalue()}</code></pre>
    </details>
    """
