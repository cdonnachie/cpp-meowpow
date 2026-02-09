#!/usr/bin/env python3

# meowpow: C/C++ implementation of Meowpow, the Meowcoin Proof of Work algorithm.
# Copyright 2019 Pawel Bylica.
# Licensed under the Apache License, Version 2.0.

import os
import subprocess
import shutil
from os import path

from setuptools import setup
from setuptools.command.build_ext import build_ext as setuptools_build_ext

try:
    from distutils.errors import CCompilerError
except Exception:  # Python 3.12+ may not have distutils
    try:
        from setuptools.errors import CompileError as CCompilerError
    except Exception:
        class CCompilerError(RuntimeError):
            pass


class build_ext(setuptools_build_ext):
    user_options = setuptools_build_ext.user_options + [
        ('skip-cmake-build', None,
         "Skip CMake build assuming the libraries are already installed " +
         "to the dist directory")
    ]

    def initialize_options(self):
        super(build_ext, self).initialize_options()
        self.skip_cmake_build = False

    def run(self):
        build_dir = path.abspath(self.build_temp)
        source_dir = path.dirname(path.abspath(__file__))
        # Keep CMake install artifacts inside the build directory so PEP517
        # isolated builds don't mutate the source tree.
        install_dir = path.join(build_dir, 'cmake-install')

        os.makedirs(build_dir, exist_ok=True)
        os.makedirs(install_dir, exist_ok=True)

        cmake_opts = [
            '-DCMAKE_INSTALL_PREFIX={}'.format(install_dir),
            '-DCMAKE_INSTALL_LIBDIR=lib',
            '-DCMAKE_POSITION_INDEPENDENT_CODE=TRUE',
            '-DHUNTER_ENABLED=OFF',
            '-DMEOWPOW_BUILD_TESTS=OFF',
            '-DMEOWPOW_INSTALL_CMAKE_CONFIG=OFF'
        ]

        # Prefer a deterministic build type for single-config generators.
        if not any(opt.startswith('-DCMAKE_BUILD_TYPE=') for opt in cmake_opts):
            cmake_opts.append('-DCMAKE_BUILD_TYPE=Release')

        generator = os.environ.get('GENERATOR')
        if generator:
            cmake_opts.append('-G{}'.format(generator))

        if not self.skip_cmake_build and not os.environ.get('MEOWPOW_PYTHON_SKIP_BUILD'):
            cmake_cmd = shutil.which('cmake')
            if not cmake_cmd:
                raise CCompilerError(
                    "cmake tool not found but required to build this package")

            r = subprocess.call([cmake_cmd, source_dir] + cmake_opts,
                                cwd=build_dir)
            if r != 0:
                raise CCompilerError(
                    "cmake configuration failed with exit status {}".format(r))
            r = subprocess.call(
                [cmake_cmd, '--build', build_dir, '--target', 'install',
                 '--config', 'Release'])
            if r != 0:
                raise CCompilerError(
                    "cmake build failed with exit status {}".format(r))

        self.library_dirs.append(path.join(install_dir, 'lib'))

        super(build_ext, self).run()


setup(
    name='meowpow',
    version='0.5.2',
    description="C/C++ implementation of Meowpow - the Meowcoin Proof of Work algorithm",
    url='https://github.com/chfast/meowpow',
    author='Pawel Bylica',
    author_email='pawel@ethereum.org',
    license='Apache License, Version 2.0',
    license_files=['LICENSE'],

    package_dir={'': 'bindings/python'},
    packages=['meowpow'],
    cffi_modules=['bindings/python/meowpow/_build.py:ffibuilder'],

    python_requires='>=3.10',
    install_requires=['cffi>=1.12'],

    test_suite='tests.test_meowpow',

    cmdclass={'build_ext': build_ext},

    classifiers=[
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: C',
        'Programming Language :: C++',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3.13',
    ],
)