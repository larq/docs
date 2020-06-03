# Contributing Guide

## Build documentation locally

Installs dependencies for building the docs:

```shell
pip install -r requirements.txt
```

Serve docs locally:

```shell
./download_lce_readme.sh
python generate_docs.py
IGNORE_MODEL_SUMMARIES=1 python -m mkdocs serve
```
## Build documentation locally using `npm`

Installs dependencies for building the docs:

```shell
npm install
```

Serve docs locally:

```shell
npm run prebuild
npm run dev
```
