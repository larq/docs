# Create an LCE inference binary for Android

!!! note
    This guide explains how to build a standalone inference binary that can be executed on an Android device using the [Android developer tools](https://developer.android.com/studio/command-line/adb#shellcommands). If you'd rather use LCE for inference as part of an Android app, please check out [this guide](/compute-engine/quickstart_android) instead.

To build Larq Compute Engine (LCE) for Android,
you must have the [Android NDK](https://developer.android.com/ndk) and
[SDK](https://developer.android.com/studio) installed on your system.
Below we explain how to install the Android prerequisites in the LCE
Docker container and how to configure the LCE Bazel build settings
accordingly. Before proceeding with the next steps, please follow
the instructions in the main [LCE build guide](/compute-engine/build/) to setup
the Docker container for LCE and the Bazel build system.

!!! note
    We recommend using the docker volume as described in the
    [LCE build guide](/compute-engine/build/) to be able to easily transfer
    files in-between the container and the host machine.

## Install prerequisites

We provide a bash script which uses the `sdkmanager` tool
to install the Android NDK and SDK inside the Docker container.
Please run the script by executing the following command from the LCE
root directory:

```bash
./third_party/install_android.sh
```

After executing the bash script, please accept the Android SDK licence agreement.
The script will download and unpack the Android NDK and SKD under the directory
`/tmp/lce_android` in the LCE docker container.

## Custom Android version

The Android NDK and SDK versions used in LCE are currently hard-coded in the
install script.
To build LCE against a different NDK and SDK versions, you can manually
modify `ANDROID_VERSION` and `ANDROID_NDK_VERSION` variables in the
install script. Additionally, the following configurations in the `.bazelrc`
file need to be adjusted:

```shell
build --action_env ANDROID_NDK_HOME="/tmp/lce_android/ndk/18.1.5063045"
build --action_env ANDROID_NDK_API_LEVEL="21"
build --action_env ANDROID_BUILD_TOOLS_VERSION="28.0.3"
build --action_env ANDROID_SDK_API_LEVEL="29"
build --action_env ANDROID_SDK_HOME="/tmp/lce_android"
```

## Build an LCE inference or benchmark binary

To build an LCE inference binary for Android (see [here](/compute-engine/inference/) for creating your
own LCE binary) the Bazel target needs to built with `--config=android_arm64` flag.
For example, to build the [minimal example](https://github.com/larq/compute-engine/blob/master/examples/lce_minimal.cc) for Android,
run the following command from the LCE root directory:

```bash
bazel build -c opt --config=android_arm64 //examples:lce_minimal
```

To build the [LCE benchmark tool](https://github.com/larq/compute-engine/tree/master/larq_compute_engine/tflite/benchmark)
for Android, simply build the bazel target
`//larq_compute_engine/tflite/benchmark:lce_benchmark_model`.

The resulting binaries will be stored at
`bazel-bin/larq_compute_engine/tflite/benchmark/lce_benchmark_model`
and `bazel-bin/examples/lce_minimal`.
The `bazel-bin` directory inside the `lce-volume` is a soft link to
the build artifacts directory outside the `lce-volume`.
As a result, in order to be able to access the inference binaries on the host machine,
you need to manually copy them from the `bazel-bin` to the `lce-volume` directory.
To do so, run the following command from the LCE root directory:

```bash
cp bazel-bin/larq_compute_engine/tflite/benchmark/lce_benchmark_model .
```
