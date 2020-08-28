# Build Larq Compute Engine for ARM

This page descibes how to build Larq Compute Engine (LCE) binaries
for 32-bit, as well as 64-bit ARM-based systems.
[Bazel](https://bazel.build/) is the primary build system for LCE and can
be used to cross-compile binaries for ARM architectures directly from the host.
To natively build on an ARM system, we provide a solution based on the
Makefile build system.

!!! warning
    Although the Raspberry Pi 3 and Raspberry Pi 4 have 64-bit CPUs, the
    officially supported OS Raspbian for the Raspberry Pi is a 32-bit OS. In order
    to use the optimized 64-bit kernels of LCE on a Raspberry Pi, a 64-bit OS such
    as [Manjaro](https://manjaro.org/download/#raspberry-pi-4-xfce) should be used.

This leaves us with three ways to build LCE binaries, which we recommend in
the following order:

1. To cross-compile LCE from a host machine, see "Cross-compiling with Bazel".
2. To natively compile LCE, see "Building with Make".
3. To cross-compile LCE using the Make system for users that do not wish to
   install Bazel, see "Cross-compiling with Make".

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

=== "Building with Make"

    To build LCE with Make, first clone the Larq Compute Engine repository and make
    sure the tensorflow submodule is loaded:

    ```bash
    git submodule update --init
    ```

    To simplify the build process for various supported targets, we provide the
    `build_lce.sh` script which accepts the build target platform as an input
    argument.

    To natively build the LCE library and C++ example programs, first you need to
    install the compiler toolchain on your target device.

    === "Linux (Debian based)"
        On Debian based systems like a
        Raspberry Pi board with Raspbian, run the following command:

        ```
        sudo apt-get install build-essential
        ```

    === "Linux (Arch based)"
        On an Arch based system like a Raspberry Pi board with Manjaro operating system, run the following command instead:

        ```
        sudo pacman -S base-devel
        ```

    You should then be able to natively compile LCE by running the following from
    the LCE root directory:

    ```bash
    larq_compute_engine/tflite/build_make/build_lce.sh --native
    ```

    It is also possible to replace `--native` by `--rpi` (32-bit ARM) or
    `--aarch64` (64-bit ARM) to add extra compiler optimization flags.

    The resulting compiled files will be stored in `gen/<TARGET>/` where,
    depending on your target platform, `<TARGET>` can be `linux_x86_64`,
    `rpi_armv7l`, or `linux_aarch64`. Here you can find the example program
    `lce_minimal` and benchmark program `lce_benchmark`.


    !!! note
        On some systems the compiler is incorrectly named `aarch64-unknown-linux-gnu-gcc`
        while it should be named `aarch64-linux-gnu-gcc`. If building with the option
        `--aarch64` results in errors then the following bash script can be used to
        create symlinks that fix this naming issue.

        ```bash
        #!/usr/bin/env bash

        cd /usr/bin
        for unknownfile in aarch64-unknown-linux-gnu-*; do
        	newfile="${unknownfile/-unknown-/-}"    
        	echo "Creating symlink $newfile that points to $unknownfile"
        	ln -s $unknownfile $newfile
        done
        ```

=== "Cross-compiling with Make"

    First clone the Larq Compute Engine repository and make sure the tensorflow
    submodule is loaded:

    ```bash
    git submodule update --init
    ```

    To cross-compile LCE, you need to first install the compiler toolchain:

    === "Linux (Debian based)"
        ```bash
        sudo apt-get update
        sudo apt-get install crossbuild-essential-arm64
        ```

    === "Linux (Arch based)"
        ```bash
        sudo pacman -Syy
        sudo pacman -S arm-linux-gnueabihf
        ```

    To build for 32-bit ARM architectures, run the following command from the LCE
    root directory:

    ```bash
    larq_compute_engine/tflite/build_make/build_lce.sh --rpi
    ```

    When building for a 64-bit ARM architecture, replace `--rpi` with `--aarch64`.

    The resulting compiled files will be stored in `gen/<TARGET>/` where,
    depending on your target platform, `<TARGET>` can be `linux_x86_64`,
    `rpi_armv7l`, or `linux_aarch64`. Here you can find the example program
    `lce_minimal` and benchmark program `lce_benchmark`.

    Copy the `benchmark_model` program to your ARM machine to run it.
