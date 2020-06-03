import tensorflow as tf
import larq_zoo as lqz
import larq as lq
import io
from functools import reduce
import os

def _generate_html(code):
    return f"""
    <details class="abstract"
      ><summary>Model Summary</summary>
      <pre class="model-summary"><code>{code}</code></pre>
    </details>
    """

def html_format(source, language=None, css_class=None, options=None, md=None, **kwargs):
    if os.getenv("IGNORE_MODEL_SUMMARIES"):
        return _generate_html("placeholder")
    model_fn = reduce(getattr, [lqz, *source.split(".")])
    stream = io.StringIO()
    tf.keras.backend.clear_session()
    lq.models.summary(model_fn(weights=None), print_fn=lambda s: print(s, file=stream))
    return _generate_html(stream.getvalue())
