# Larq Compute Engine Android Quickstart

This guide consists of two main sections. In the [first section](#Create-Your-Own-Android-app-using-LCE-and-TensorFlow-Lite),
we describe how to build your own Android app using Larq Compute Engine (LCE) and
[TensorFlow Lite Java Inference APIs](https://www.tensorflow.org/lite/guide/inference#load_and_run_a_model_in_java)
to perform inference with a model built and trained with [Larq](https://larq.dev). 
This can be achieved either by using our pre-built [LCE Lite AAR hosted on Bintray](https://bintray.com/plumeraihq/larq-compute-engine)
(see [here](#Use-the-LCE-AAR-from-Bintray) for instructions) or you can build the LCE Lite AAR on
your local machine by following the guide [here](#Build-LCE-AAR-locally).
In the [second section](#Build-an-LCE-inference-binary), we describe how to build
a LCE-compatible inference binary that can be executed on Android OS
(e.g, a binary to benchmark your models).

## Create Your Own Android app using LCE and TensorFlow Lite ##
In this section, we demonstrate how to perform inference with a Larq model in an
Android app. We provide a custom LCE-compatible TensorFlow Lite [Android Archive](https://developer.android.com/studio/projects/android-library) (AAR)
which you can use in your own Android app to perform inference with the [TensorFlow Lite Java inference APIs](https://www.tensorflow.org/lite/guide/inference#load_and_run_a_model_in_java).
In this guide, we use the [TensorFlow Lite Android image classification app](https://github.com/tensorflow/examples/tree/master/lite/examples/image_classification/android)
as an example.
To get started with TensorFlow Lite on Android, we recommend to carefully read the
TensorFlow Lite [Android quickstart](https://www.tensorflow.org/lite/guide/android)
before proceeding with the next steps in this guide.

### 1. Build in Android Studio ###

To download and build the TensorFlow Lite Android image classification app
in [Android Studio](https://developer.android.com/studio), follow the instructions
[here](https://github.com/tensorflow/examples/blob/master/lite/examples/image_classification/android/README.md).
For an explanation of the source code,
see [here](https://github.com/tensorflow/examples/blob/master/lite/examples/image_classification/android/EXPLORE_THE_CODE.md).

### 2. Add LCE-compatible TensorFlow Lite AAR to the project ###
To add the LCE Lite AAR to your android project, you can either use the pre-built
[LCE Lite AAR hosted on Bintray]((https://bintray.com/plumeraihq/larq-compute-engine))
or build the LCE Lite AAR yourself on your local machine. Both approaches are explained
in detail in the following sections.

#### Use the LCE Lite AAR from Bintray ####
To use LCE Lite AAR in the android app, we recommend using the
[LCE package hosted at Bintray](https://bintray.com/plumeraihq/larq-compute-engine).
Modify the `build.gradle` file in the anroid project to include the
`lce-lite` dependency:

```
allprojects {
    repositories {
        maven {
            url  "https://dl.bintray.com/plumeraihq/larq-compute-engine"
        }
    }
}

dependencies {
    implementation 'org.larq:lce-lite:0.1.2'
}
```

This AAR includes binaries for `arm64-v8a`, `x86_64`, `x86` [Android ABIs](https://developer.android.com/ndk/guides/abis).
Please note that currently hand-optimized LCE operators are available only for `arm64-v8a`.
To include binaries only for Android ABIs you need to support, modify `abiFilters`
in the Gradle build as described [here](https://www.tensorflow.org/lite/guide/android#use_the_tensorflow_lite_aar_from_jcenter).

!!! note
    In TensorFlow Lite image classification app, you need to also remove
    the standard TensorFlow Lite dependency by commenting out the following
    line in `build.gradle` file:

    ```
    dependencies {
        // Comment out the following line
        // implementation 'org.tensorflow:tensorflow-lite:0.0.0-nightly'
    }
    ```
    Note that the dependencies `tensorflow-lite-gpu` and `tensorflow-lite-support` are still required!

#### Build LCE Lite AAR locally ####

In cases that you would like to make local changes to the LCE code or
TensorFlow Lite binaries, you might wish to build the LCE Lite AAR locally.
We provide a bash script to build the LCE Lite AAR. The bash script is only
tested inside the LCE docker container. See LCE [build guide](/compute-engine/build) to
setup the docker container.

Once the docker container is setup, run the following command from the LCE root
directory inside the container:

``` bash
./larq_compute_engine/tflite/java/build_lce_aar.sh
```
The script will build the LCE Android archive `lce-lite-<version>.aar` and
store the file in the root directory of LCE repository.

Transfer the LCE Android archive file from the LCE container to the host
machine (where the Android Studio is setup).
Execute the following command to install the LCE Android Archive
to local [Maven](https://maven.apache.org) repository:

```
mvn install:install-file \
  -Dfile=lce-lite-0.1.2.aar \
  -DgroupId=org.larq \
  -DartifactId=lce-lite -Dversion=0.1.000 -Dpackaging=aar
```

Modify the `build.gradle` file in the the Android project to
include `mavenLocal()` repository:

```
allprojects {
    repositories {
        jcenter()
        mavenLocal()
    }
}
```

Replace the standard TensorFlow Lite dependency with
local LCE Lite AAR:

```
dependencies {
    implementation 'org.larq:lce-lite:0.1.000'
}
```

Note that the version `0.1.000` is chosen arbitrarily and should match the version
passed to the `-Dversion` argument in Maven command executed previously.

### 3. Add Larq Model to the project ###

In this guide, we use the Larq [QuickNet](https://docs.larq.dev/zoo/api/sota/#quicknet)
model for efficient and fast image classification. The FlatBuffer format of the QuickNet model
`quicknet.tflite` can be created by using the [LCE converter](/compute-engine/converter)
and needs to be placed in the `assets` folder of the Android project.
You also need to use the `labels_without_background.txt` as its corresponding labels file.
The labels file is already available in the `asset` folder of
the TensorFlow Lite image classification Android app.

The TensorFlow Lite classifier in the image classifaction app works with the
float MobileNet model. To replace the MobileNet with QuickNet, you need to modify
`getModelPath()` and `getLabelPath()` methods in `ClassifierFloatMobileNet.java`
file.

``` java
@Override
protected String getModelPath() {
    return "quicknet.tflite";
}

@Override
protected String getLabelPath() {
    return "labels_without_background.txt";
}
```

The QuickNet model requires additional normalization of the input by changing
the `IMAGE_MEAN` and `IMAGE_STD` variables in `ClassifierFloatMobileNet` class:

``` java
private static final float[] IMAGE_MEAN = {0.485f * 255, 0.456f * 255, 0.406f * 255};
private static final float[] IMAGE_STD = {0.229f * 255, 0.224f * 255, 0.225f * 255};
```

Now you will be able to build the App in Android Studio and run it on your Android phone.
Choose the `Float` model in the app drop-down list to use QuickNet for inference.
The following screenshot shows an example of image classification using LCE Lite AAR as 
the inference engine.

<img src="/images/image_class_schroedi.png" width="300">

## Create an LCE inference binary for Android ##

To build Larq Compute Engine (LCE) for Android,
you must have the [Android NDK](https://developer.android.com/ndk) and
[SDK](https://developer.android.com/studio) installed on your system.
Below we explain how to install the Android prerequisites in the LCE
Docker container and how to configure the LCE Bazel build settings
accordingly. Before proceeding with the next steps, please follow
the instructions in the main [LCE build guide](/compute-engine/build) to setup
the Docker container for LCE and the Bazel build system.

NOTE: we recommend using the docker volume as described in the
[LCE build guide](/compute-engine/build) to be able to easily transfer
files in-between the container and the host machine.

##### Install prerequisites #####

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

##### Custom android version #####

The Android NDK and SDK versions used in LCE are currently hard-coded in the
install script.
To build LCE against a different NDK and SDK versions, you can manually
modify `ANDROID_VERSION` and `ANDROID_NDK_VERSION` variables in the
install script. Additionally, the following configurations in `configure.sh`
(or `.bazelrc`) file need to be adjusted:

```shell
build --action_env ANDROID_NDK_HOME="/tmp/lce_android/ndk/19.2.5345600"
build --action_env ANDROID_NDK_API_LEVEL="21"
build --action_env ANDROID_BUILD_TOOLS_VERSION="28.0.3"
build --action_env ANDROID_SDK_API_LEVEL="23"
build --action_env ANDROID_SDK_HOME="/usr/local/android/android-sdk-linux"
```

### Build an LCE inference binary ###

To build an LCE inference binary for Android (see [here](/compute-engine/inference) for creating your
own LCE binary) the Bazel target needs to built with `--config=android_arm64` flag.
For example, to build the [minimal example](https://github.com/larq/compute-engine/blob/master/examples/lce_minimal.cc) for Android,
run the following command from the LCE root directory:

```bash
bazel build -c opt \
    --config=android_arm64 \
    //examples:lce_minimal
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

In the next section, we describe how to transfer and execute the inference binaries
on your Android device.

##### Run inference #####

To run the inference with a [Larq converted model](/compute-engine/converter) on an Android phone,
please follow these steps on your host machine (replace the `lce_benchmark_model` with your
desired inference binary):

(1) Install the [Android Debug Bridge (adb)](https://developer.android.com/studio/command-line/adb) on your host machine.

(2) Follow the instructions [here](https://developer.android.com/studio/debug/dev-options#enable)
to enable `USB debugging` on your Android phone.

(3) Connect your phone and run the following command to confirm that your host
computer is connected to the phone:

```bash
adb devices
```

(4) Transfer the LCE inference binary to your phone:

```bash
adb push lce_benchmark_model  /data/local/tmp
```

(5) Make the binary executable:

```shell
adb shell chmod +x /data/local/tmp/lce_benchmark_model
```

(6) Transfer the converted `.tflite` model file to your phone:

```shell
adb push binarynet.tflite /data/local/tmp
```

(7) Run the inference:

```shell
adb shell /data/local/tmp/lce_benchmark_model \
    --graph=/data/local/tmp/binarynet.tflite \
    --num_threads=4
```
