# MNI Xfm Transformations

[![Version](https://img.shields.io/docker/v/fnndsc/pl-xfm?sort=semver)](https://hub.docker.com/r/fnndsc/pl-xfm)
[![MIT License](https://img.shields.io/github/license/fnndsc/pl-xfm)](https://github.com/FNNDSC/pl-xfm/blob/main/LICENSE)
[![ci](https://github.com/FNNDSC/pl-xfm/actions/workflows/ci.yml/badge.svg)](https://github.com/FNNDSC/pl-xfm/actions/workflows/ci.yml)

`pl-xfm` is a [_ChRIS_](https://chrisproject.org/)
_ds_ plugin which takes in `.obj` and `.mnc` files
from an input directory, applies the linear transformation
specified by its arguments, and writes the results
to an output directory.

## Installation

`pl-xfm` is a _[ChRIS](https://chrisproject.org/) plugin_, meaning it can
run from either within _ChRIS_ or the command-line.

[![Get it from chrisstore.co](https://ipfs.babymri.org/ipfs/QmaQM9dUAYFjLVn3PpNTrpbKVavvSTxNLE5BocRCW1UoXG/light.png)](https://chrisstore.co/plugin/pl-xfm)

## Local Usage

To get started with local command-line usage, use [Apptainer](https://apptainer.org/)
(a.k.a. Singularity) to run `pl-xfm` as a container.

To print its available options, run:

```shell
singularity exec docker://fnndsc/pl-xfm cxfm --help
```

## Examples

To scale every object inside a directory named `incoming/`
to be larger by a factor of 2, run

```shell
singularity exec docker://fnndsc/pl-xfm cxfm --scale 2.0 incoming/ outgoing/
```

### Sample Data

- https://github.com/aces/surface-extraction/tree/97a1ebe08c716e651531eddda949d8fa6ce8f0f1/models
- https://github.com/aces/CIVET_Full_Project/blob/master/Test/mni_icbm_00100_t1.mnc
