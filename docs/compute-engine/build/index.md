# Build Larq Compute Engine

The Larq Compute Engine (LCE) repository consists of two main components:

- **LCE Runtime:** which is a collection of highly optimized
  [TensorFlow Lite](https://www.tensorflow.org/lite) custom operators.

- **LCE Converter:** which takes a Larq model and generates a TensorFlow Lite
  [FlatBuffer](https://google.github.io/flatbuffers/) file (`.tflite`) compatible
  with the LCE runtime.

!!! important
    Make sure to checkout the `git` tag matching the version of the
    [LCE converter](/compute-engine/api/python/) used to convert the model:
    ```
    git checkout v0.4.3
    ```
    If you have installed the converter from PyPI you can check the
    currently installed version using:
    ```
    pip freeze | grep larq-compute-engine
    ```

## Setup the build environment

[Bazel](https://bazel.build/) is the primary build system for LCE.
However, to avoid Bazel compatibility issues, you need to use [Bazelisk](https://github.com/bazelbuild/bazelisk)
as a launcher for Bazel.

=== "Linux"
    To install Bazelisk on Linux, run the following two commands
    (replace `v1.6.1` with your preferred
    [bazelisk version](https://github.com/bazelbuild/bazelisk/releases)):

    ```shell
    sudo wget -O /usr/local/bin/bazel \
        https://github.com/bazelbuild/bazelisk/releases/download/v1.6.1/bazelisk-linux-amd64
    sudo chmod +x /usr/local/bin/bazel
    ```

=== "macOS"
    To install Bazelisk on MacOS, run:
    ```
    brew install bazelisk
    ```

## Build LCE Runtime

The LCE runtime has a diverse platform support, covering
[Android](/compute-engine/quickstart_android/) and [ARM-based boards](/compute-engine/build/arm/)
such as Raspberry Pi. To build/install/run LCE runtime on
each of these platforms, please refer to the corresponding guide.

## Build LCE Converter

The [LCE converter](/compute-engine/api/python/) is available on [PyPI](https://pypi.org/project/larq-compute-engine/)
and can be installed with Python's [pip](https://pip.pypa.io/en/stable/)
package manager:

```shell
pip install larq-compute-engine
```

To build the LCE pip package yourself, refer to [building the converter](/compute-engine/build/converter/).
