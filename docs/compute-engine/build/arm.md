# Build Larq Compute Engine for ARM

This page descibes how to build Larq Compute Engine (LCE) binaries
for 32-bit, as well as 64-bit ARM-based systems.
[Bazel](https://bazel.build/) is the primary build system for LCE and can
be used to cross-compile binaries for ARM architectures directly from the host.
To natively build on an ARM system, we provide a solution based on the
Makefile build system.

!!! warning
    Although the Raspberry Pi 3 and Raspberry Pi 4 have 64-bit CPUs, the default version of Raspberry Pi OS (previously known as Raspbian) is 32-bit. In order
    to use the optimized 64-bit kernels of LCE on a Raspberry Pi, the 64-bit version should be used,
    see [here](https://www.raspberrypi.com/software/operating-systems/) under 'Raspberry Pi OS (64-bit)'.

This leaves us with three ways to build LCE binaries, which we recommend in
the following order:

1. To cross-compile LCE from a host machine, see "Cross-compiling with Bazel".
2. To natively compile LCE, see "Building with CMake".
3. To cross-compile LCE using the CMake system for users that do not wish to
   install Bazel, see "Cross-compiling with CMake".

This guide will show you how to build the [LCE example program](https://github.com/larq/compute-engine/blob/master/examples/lce_minimal.cc).
See [here](/compute-engine/inference/) to find out how you can create your own LCE
inference binary.

=== "Cross-compiling with Bazel"

    For cross-compiling on a Mac host, a Docker image is required.
    Please see [setting up Docker](/compute-engine/build/docker/) for instructions on
    setting up the Docker container, and then follow continue the steps here.

    To cross-compile the LCE example for ARM architectures, the bazel
    target needs to be built with the `--config=rpi3` (32-bit ARM) or
    `--config=aarch64` (64-bit ARM) flag. For example, to build the example
    for 64-bit ARM systems, run the following command from the LCE root
    directory:

    ```bash
    bazel build --config=aarch64 //examples:lce_minimal
    ```

    To build the LCE benchmark tool, build the bazel target
    `//larq_compute_engine/tflite/benchmark:lce_benchmark_model`

    The resulting binaries will be stored at
    `bazel-bin/examples/lce_minimal` and
    `bazel-bin/larq_compute_engine/tflite/benchmark/lce_benchmark_model`. You can
    copy these to your ARM machine and run them there.

=== "Building with CMake"

    To build LCE with CMake, first clone the Larq Compute Engine repository and make
    sure the tensorflow submodule is loaded:

    ```bash
    git submodule update --init
    ```

    To natively build the LCE library and C++ example programs, first you need to
    install the compiler toolchain on your target device.

    === "Linux (Debian based)"
        On Debian based systems like a
        Raspberry Pi board with Raspberry Pi OS (previously known as Raspbian), run the following command:

        ```
        sudo apt-get install cmake build-essential
        ```

    === "Linux (Arch based)"
        On an Arch based system like a Raspberry Pi board with Manjaro operating system, run the following command instead:

        ```
        sudo pacman -S base-devel cmake
        ```

    You should then be able to natively compile LCE by running the following from
    the LCE root directory:

    ```bash
    cmake -S . -B build
    cmake --build build
    ```

    Here 'build' is the name of the out-of-source build directory chosen,
    which will have all the intermediate and resulting files.
    Here you can find the example program
    `example` and benchmark program `lce_benchmark_model`.


=== "Cross-compiling with CMake"

    First clone the Larq Compute Engine repository and make sure the tensorflow
    submodule is loaded:

    ```bash
    git submodule update --init
    ```

    To cross-compile LCE, you need to first install the compiler toolchain:

    === "Linux (Debian based)"
        ```bash
        sudo apt-get update
        sudo apt-get install crossbuild-essential-armhf crossbuild-essential-arm64
        ```
        The `-armhf` package is for 32-bit ARM, the `-arm64` package for 64-bit ARM.

    === "Linux (Arch based)"
        ```bash
        sudo pacman -Syy
        sudo pacman -S arm-linux-gnueabihf aarch64-linux-gnu-gcc
        ```
        The first package is for 32-bit ARM, the second one for 64-bit ARM.

    To cross-compile, run the following command from the LCE
    root directory:

    ```bash
    export CC=/path/to/gcc-arm-<X>.<Y>-x86_64-<ARCH>-none-linux-gnu/bin/<ARCH>-none-linux-gnu-gcc
    export CXX=/path/to/gcc-arm-<X>.<Y>-x86_64-<ARCH>-none-linux-gnu/bin/<ARCH>-none-linux-gnu-g++
    cmake -S . -B build
    cmake --build build -j4
    ```

    Here the paths to the compiler are dependent on whether you are targeting 32-bit or 64-bit ARM. Change these paths to match the ARM cross-compiler installed on your system.

    Here 'build' is the name of the out-of-source build directory chosen,
    which will have all the intermediate and resulting files.
    Here you can find the example program
    `example` and benchmark program `lce_benchmark_model`.

    Copy the `benchmark_model` program to your ARM machine to run it.
