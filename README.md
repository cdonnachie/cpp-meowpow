# Meowpow

[![readme style standard](https://img.shields.io/badge/readme%20style-standard-brightgreen.svg?style=flat-square)](https://github.com/RichardLitt/standard-readme)

> C/C++ implementation of Meowpow – the Meowcoin Proof of Work algorithm


## Table of Contents

- [Install](#install)
- [Usage](#usage)
- [Test vectors](#test-vectors)
- [Optimizations](#optimizations)
- [Maintainer](#maintainer)
- [License](#license)


## Install

Build from source using CMake.

```sh
mkdir build
cd build
cmake ..
cmake --build .
```

### Python wheel (PyPI)

This repo includes Python bindings (CFFI) and can build a binary wheel.

```sh
py -m pip install -U build
py -m build -w
```

The wheel will be written to the `dist/` directory.

Note: building a wheel requires a working C/C++ toolchain and CMake.

#### Multiple Python versions (3.10–3.13)

Binary wheels are Python-version-specific (e.g. cp310, cp311, ...). To build a
set of wheels for multiple Python versions, use `cibuildwheel`:

```sh
py -m pip install -U cibuildwheel
py -m cibuildwheel --output-dir dist
```

## Usage

See [meowpow.hpp] for list of exported function and documentation.


## Test vectors

- [ProgPoW test vectors](test/unittests/progpow_test_vectors.hpp)


## Optimizations

This section decscribes the optimizations, modification and tweaks applied
in this library in relation to [Meowpow reference implementation].

The library contains a set of micro-benchmarks. Build and run `bench` tool.

### Seed hash is computed on the fly.
   
Seed hash is sequence of keccak256 hashes applied the epoch number of times.
Time needed to compute seed hash is negligible comparing to time needed to build
light cache. Computing seed hash for epoch 10000 takes ~ 5 ms, building light
cache for epoch 1 takes ~ 500 ms.

### Dataset size is computed on the fly

Computing the size of full dataset and light cache requires finding the largest
prime number given an upper bound. For similar reasons as with seed hash, this
is computed on the fly. The procedure used is quite naive and forks well only
up to 40-bit number, so some additional improvement can be done in future.
   
    
## Maintainer

Paweł Bylica [@chfast]

## License

Licensed under the [Apache License, Version 2.0].


[@chfast]: https://github.com/chfast
[Apache License, Version 2.0]: LICENSE
[meowpow.hpp]: include/meowpow/meowpow.hpp
[Meowpow reference implementation]: https://github.com/ethereum/wiki/wiki/Meowpow
