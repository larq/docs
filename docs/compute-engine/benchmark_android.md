# Benchmark models on Android

This guide will walk you through how to benchmark a [Larq converted model](/compute-engine/api/converter/) on your Android phone.

1. Install the [Android Debug Bridge (adb)](https://developer.android.com/studio/command-line/adb) on your host machine.
   On macOS you can install it via `brew`:
   ```
   brew cask install android-platform-tools
   ```

2. Follow the instructions [here](https://developer.android.com/studio/debug/dev-options#enable)
to enable `USB debugging` on your Android phone.

3. Connect your phone and run the following command to confirm that your host
computer recognises your phone:
   ```
   adb devices
   ```

4. Download the prebuilt Android benchmarking binary from the [latest release](https://github.com/larq/compute-engine/releases/latest). <!-- TODO add wget or curl command once we've published the 0.4 -->

5. Transfer the LCE inference binary to your phone:
   ```
   adb push lce_benchmark_model_android_arm64 /data/local/tmp
   ```

6. Transfer the converted `.tflite` model file to your phone:
   ```
   adb push quicknet.tflite /data/local/tmp
   ```

7. Benchmark the model:
   ```
   adb shell /data/local/tmp/lce_benchmark_model_android_arm64 \
       --graph=/data/local/tmp/quicknet.tflite \
       --num_threads=4
   ```
   Add `--help` to the command for a detailed description of the available benchmarking options.
   <!-- TODO do we need to make it executable first -->
