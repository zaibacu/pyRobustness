#!/usr/bin/python
# -*- coding: UTF-8 -*-
from setuptools import setup
try:
    from pip._internal.req import parse_requirements
except:
    from pip.req import parse_requirements

from robust.version import get_version

install_reqs = list(parse_requirements("requirements.txt", session={}))

with open("README.md", "r") as f:
    long_description = f.read()


setup(name="pyrobustness",
      version=get_version(),
      description="A simple util library for creating applications which needs to keep running, despite abnormalities",
      long_description=long_description,
      long_description_content_type="text/markdown",
      author="Šarūnas Navickas",
      author_email="zaibacu@gmail.com",
      license="MIT",
      url="https://github.com/zaibacu/pyRobustness",
      packages=["robust"],
      install_requires=[str(ir.req) for ir in install_reqs],
      test_suite="pytest",
      tests_require=["pytest"])
