# Contributing Guide

## Build documentation locally

Installs dependencies for building the docs:

```shell
pip install -r requirements.txt
```

Serve docs locally:

```shell
./download_lce_readme.sh
python generate_api_docs.py
python -m mkdocs serve
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
