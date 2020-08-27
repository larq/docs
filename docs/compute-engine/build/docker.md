# Docker container for LCE builds

It is usually not needed to build LCE in a [Docker](https://www.docker.com/)
container, and we recommend first following
[this guide (benchmark binaries)](/compute-engine/build/arm/) or
[this guide (converter)](/compute-engine/build/converter/)
to try and build LCE outside of a Docker container.

There are scenarios in which building in the Docker container is preferred:
- To build a [`manylinux2010`](https://www.python.org/dev/peps/pep-0571/)-compatible pip package
- To build a benchmark binary for Android
- When the build outside of the container fails and can't be fixed.

We recommend to use [Docker volumes](https://docs.docker.com/storage/volumes/)
to migrate the build targets in-between the host machine and the container.

To be able to build the LCE converter's
[`manylinux2010`](https://www.python.org/dev/peps/pep-0571/) compatible PIP
package, we need to use the
[`tensorflow:custom-op-ubuntu16`](https://hub.docker.com/r/tensorflow/tensorflow)
image.

First, download the Docker image:

```bash
docker pull tensorflow/tensorflow:custom-op-ubuntu16
```

Clone the LCE repository on the host machine:

```bash
mkdir lce-volume
git clone https://github.com/larq/compute-engine.git lce-volume
```

Start the container and map the `lce-volume` directory to the `/tmp/lce-volume`
directory inside the container:

```bash
docker run -it -v $PWD/lce-volume:/tmp/lce-volume \
    -w /tmp/lce-volume tensorflow/tensorflow:custom-op-ubuntu16 /bin/bash
```

Now, you will be able to build bazel targets inside the container, by following
the normal build instructions. Some build artifacts are stored in the
`bazel-bin` folder which is not visible from from outside the Docker container.
Simply copy a file from `bazel-bin` into the main folder `/tmp/lce-volume` to
be able to access it.

## Building a manylinux2010 pip package

To make the larq-compute-engine pip package `manylinux2010` compatible, some
extra setup steps need to be taken, which have been collected in
[this script](https://github.com/larq/compute-engine/blob/master/.github/tools/release_linux.sh).

We recommend running this as follows, from inside the Docker container. Please
change the Python verion to the desired version:

```bash
cd /tmp/lce-volume
export PYTHON_VERSION="3.8"
.github/tools/release_linux.sh
```

The `.whl` file will then be available in the `artifacts` folder, and it can be
installed on the host system.
