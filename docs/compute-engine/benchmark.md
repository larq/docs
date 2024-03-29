# Benchmark models

Larq Compute Engine provides prebuilt binaries to benchmark [Larq converted models](/compute-engine/api/python/) on Android phones or 64-bit ARM based systems like the Raspberry Pi.

=== "Raspberry Pi (64-bit)"

    1. Download the prebuilt benchmarking binary from the [latest release](https://github.com/larq/compute-engine/releases/latest):
       ```
       wget https://github.com/larq/compute-engine/releases/download/v0.7.0/lce_benchmark_model_aarch64 -O lce_benchmark_model
       ```

    2. Make the binary executable:
       ```
       chmod +x lce_benchmark_model
       ```

    3. Benchmark the converted `.tflite` model:
       ```
       ./lce_benchmark_model --graph=quicknet.tflite --num_threads=4
       ```
       Add `--help` to the command for a detailed description of the available benchmarking options.

=== "Android phone"

    1. Install the [Android Debug Bridge (adb)](https://developer.android.com/studio/command-line/adb) on your host machine. E.g. on macOS you can install it via `brew`:
       ```
       brew cask install android-platform-tools
       ```

    2. Follow the instructions [here](https://developer.android.com/studio/debug/dev-options#enable)
    to enable "USB debugging" on your Android phone.

    3. Connect your phone and run the following command to confirm that your host
    computer recognises your phone:
       ```
       adb devices
       ```

    4. Download the prebuilt Android benchmarking binary from the [latest release](https://github.com/larq/compute-engine/releases/latest):
       ```
       wget https://github.com/larq/compute-engine/releases/download/v0.7.0/lce_benchmark_model_android_arm64 -O lce_benchmark_model
       ```

    5. Transfer the LCE inference binary to your phone:
       ```
       adb push lce_benchmark_model /data/local/tmp
       ```

    6. Transfer the converted `.tflite` model file to your phone:
       ```
       adb push quicknet.tflite /data/local/tmp
       ```

    7. Make the binary executable:
       ```
       adb shell chmod +x /data/local/tmp/lce_benchmark_model
       ```

    8. Benchmark the model:
       ```
       adb shell /data/local/tmp/lce_benchmark_model \
           --graph=/data/local/tmp/quicknet.tflite \
           --num_threads=4
       ```
       Add `--help` to the command for a detailed description of the available benchmarking options.
