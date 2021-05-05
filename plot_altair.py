import inspect
import os
import uuid

import numpy as np
import tensorflow as tf

import altair as alt
import larq as lq
import pandas as pd


def calculate_activation(function, x):
    tf_x = tf.Variable(x)
    with tf.GradientTape() as tape:
        activation = function(tf_x)
    return activation.numpy(), tape.gradient(activation, tf_x).numpy()


def html_format(source, language=None, css_class=None, options=None, md=None, **kwargs):
    div_id = f"altair-plot-{uuid.uuid4()}"
    return f"""
<div id="{ div_id }">
  <script>
    function render(event) {{
      if (document.getElementById("{ div_id }")) {{
        var opt = {{
          mode: "vega-lite",
          renderer: "canvas",
          actions: false
        }};
        vegaEmbed("#{ div_id }", "{source}", opt).catch(console.err);
      }}
    }}

    // embed when document is loaded, to ensure vega library is available
    document.addEventListener("DOMContentLoaded", render, {{
      passive: true,
      once: true
    }});

    // Re-render Vega chart on document switch (instant loading, custom event)
    document.addEventListener("DOMContentSwitch", render, {{
      passive: true,
      once: true
    }});
  </script>
</div>
"""


def plot_activation(
    source, language=None, css_class=None, options=None, md=None, **kwargs
):
    function = eval("lq." + source)
    if inspect.isclass(function):
        function = function()
    x = np.linspace(-2, 2, 500)
    y, dy = calculate_activation(function, x)
    data = pd.DataFrame({"x": x, "y": y, "dy / dx": dy})

    base = alt.Chart(data, width=280, height=180).mark_line().encode(x="x")
    forward = base.encode(y="y").properties(title="Forward pass")
    backward = base.encode(y="dy / dx").properties(title="Backward pass")

    base_path = os.path.join(os.path.dirname(__file__), "docs", "plots", "generated")
    os.makedirs(base_path, exist_ok=True)
    file_name = f"{source}.vg.json"
    file_path = os.path.join(base_path, file_name)

    json_data = (forward | backward).to_json(indent=None)
    try:
        with open(file_path, "r") as f:
            old_data = f.read()
        if json_data != old_data:
            raise ValueError("Old file, should regenerate")
    except (FileNotFoundError, OSError, ValueError):
        with open(file_path, "w") as f:
            f.write(json_data)
    return html_format(f"/plots/generated/{file_name}")
