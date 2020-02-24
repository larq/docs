#!/usr/bin/env bash
set -e
basedir=`dirname $0`

# Fetch compute-engine README
echo "# Larq Compute Engine" > $basedir/docs/compute-engine/index.md
curl https://raw.githubusercontent.com/larq/compute-engine/master/README.md | tail -n +4 >> $basedir/docs/compute-engine/index.md
