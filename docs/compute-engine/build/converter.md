# Building the converter

To build the pip package with the converter, Bazel needs to know for which
Python version to build the package.
You can set this through the environment variable `TF_PYTHON_VERSION`, for example

```bash
export TF_PYTHON_VERSION="3.12"
```

If you have run Bazel without setting the python version, or you want to change
the version, you have to make Bazel re-detect the Python version. This requires
a full clean, a normal `clean` is not enough to trigger the redetection:

```bash
bazel clean --expunge
```

To build the pip package, now simply run

```bash
bazel build :build_pip_pkg
bazel-bin/build_pip_pkg artifacts
```

If you get an error about a `@pypi_lce_XXXXX` package, then it can help to
re-generate the `requirements.txt` file that Bazel uses. To do so, run

```bash
pip-compile --allow-unsafe --no-emit-index-url --strip-extras larq_compute_engine/requirements.in
```

After the bazel build is finished, the script stores the wheel file in the
`artifacts/` directory located in the LCE root directory. To install the PIP package:

```bash
pip install artifacts/*.whl
```

To build a [`manylinux2010`](https://www.python.org/dev/peps/pep-0571/)-compatible
pip package, follow the steps in [this guide](/compute-engine/build/docker/).
