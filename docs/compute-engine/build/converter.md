# Building the converter

To build the pip package with the converter, Bazel needs to know for which
python version to build the package.
If you are using a python virtual environment, please run bazel from that
environment, as Bazel will automatically detect the python version of the
virtual environment.

Bazel will detect the python version the first time you try to build anything
that requires python. If you have run Bazel outside of your virtual
environment and now want to run it in the environment, you have to make Bazel
re-detect the python verion. This requires a full clean, a normal `clean` is
not enough to trigger the redetection.:

```bash
bazel clean --expunge
```

Install the TensorFlow pip package to ensure that all required dependencies
are available:
```bash
pip install tensorflow
```

To build the pip package, now simply run

```bash
bazel build :build_pip_pkg
bazel-bin/build_pip_pkg artifacts
```

The script stores the wheel file in the `artifacts/` directory located in the
LCE root directory. To install the PIP package:

```bash
pip install artifacts/*.whl
```

To build a [`manylinux2010`](https://www.python.org/dev/peps/pep-0571/)-compatible
pip package, follow the steps in [this guide](/compute-engine/build/docker/).
