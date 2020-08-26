# Getting started
These steps will walk you through deploying a BNN with LCE. The guide starts by downloading, converting and benchmarking a model from [Larq Zoo](https://docs.larq.dev/zoo/), and will then discuss the process for a custom model.

## 1. Picking a model from Larq Zoo
This example uses the [QuickNet model](https://docs.larq.dev/zoo/api/sota/#quicknet) from the `sota` submodule of `larq-zoo`.
First, install the Larq Ecosystem pip packages:
```bash
pip install larq larq-zoo larq-compute-engine
```

Then, create a python script that will download QuickNet and print the model summary:
```python
import larq as lq
import larq_compute_engine as lce
import larq_zoo as lqz


# Load the QuickNet architecture and download the weights for ImageNet
model = lqz.sota.QuickNet(weights="imagenet")
lq.models.summary(model)
model.save("quicknet.h5")
```
*output:*
```
+quicknet summary-----------------------------+
| Total params                      10.5 M    |
| Trainable params                  10.5 M    |
| Non-trainable params              7.3 k     |
| Model size                        3.18 MiB  |
| Model size (8-bit FP weights)     1.69 MiB  |
| Float-32 Equivalent               40.10 MiB |
| Compression Ratio of Memory       0.08      |
| Number of MACs                    1.25 B    |
| Ratio of MACs that are binarized  0.9960    |
+---------------------------------------------+
```
As you can see, the model size is 3.18 MiB, but the float-32 model size is 40.10 MiB. Indeed, if you look at the `quicknet.h5` file you just saved, you'll see that it is around 42 MiB in size. This is because the model is currently unoptimized and the weights are still stored as floats rather than binary values, so executing this model on any device wouldn't be very fast at all. 

## 2. Converting the model
Larq Compute Engine is built on top of TensorFlow Lite, and therefore uses the [TensorFlow Lite FlatBuffer format](https://google.github.io/flatbuffers/) to convert and serialize Larq models for inference. We provide our own [LCE Model Converter](https://docs.larq.dev/compute-engine/api/converter/) to convert models from Keras to flatbuffers, containing additional optimization passes that increase the execution speed of Larq models on the supported target platforms. 

Using this converter is very simple, and can be done by adding the following code to the python script above:
```python
with open("quicknet.tflite", "wb") as flatbuffer_file:
    # Convert our Keras model to a TFLite flatbuffer file
    flatbuffer_bytes = lce.convert_keras_model(model)
    flatbuffer_file.write(flatbuffer_bytes)
```
This will produce the converted `quicknet.tflite` file with compressed weights and optimized operations, which is only just over 3 MiB in size!

## 3. Benchmarking
This part of the guide assumes that you'll want to benchmark on an Arm-64 based board such as a Raspberry Pi. For more detailed instructions on benchmarking, see the [Benchmarking guide](https://docs.larq.dev/compute-engine/benchmark).

On Arm64, benchmarking is as simple as downloading the pre-built benchmarking binary from the [latest release](https://github.com/larq/compute-engine/releases/latest) to the target device and running it with the converted model:
```shell
wget <TODO-URL> -o benchmark_model
chmod +x benchmark_model
./benchmark_model --graph=quicknet.tflite --num_runs=50 --num_threads=1
```

This will benchmark the model over 50 runs, using a single CPU thread, and will print output similar to the following:
```
STARTING!
Duplicate flags: num_threads
Min num runs: [50]
Min runs duration (seconds): [1]
Max runs duration (seconds): [150]
Inter-run delay (seconds): [-1]
Num threads: [1]
...
...
Loaded model quicknet.tflite
The input model file size (MB): 3.34914
Initialized session in 3.501ms.
Running benchmark for at least 1 iterations and at least 0.5 seconds but terminate if exceeding 150 seconds.
count=12 first=156677 curr=33205 min=32578 max=156677 avg=43268.1 std=34197

Running benchmark for at least 50 iterations and at least 1 seconds but terminate if exceeding 150 seconds.
count=50 first=33228 curr=33130 min=32687 max=33239 avg=33071.8 std=129

Inference timings in us: Init: 3501, First inference: 156677, Warmup (avg): 43268.1, Inference (avg): 33071.8
```
The number of interest here is `Inference (avg)`, which in this case is 33.1 ms (33071.8 microseconds) on a [Raspberry Pi 4B](https://www.raspberrypi.org/documentation/hardware/raspberrypi/bcm2711/README.md).

To see the other available benchmarking options, add `--help` to the command above.

## 4. Create your own Larq model
TODO
