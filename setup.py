#!/usr/bin/python
# -*- coding: UTF-8 -*-
from setuptools import setup
from pip.req import parse_requirements
from pip.exceptions import InstallationError

from robust.version import get_version

try:
    install_reqs = list(parse_requirements("requirements.txt", session={}))
except InstallationError:
    # There are no requirements
    install_reqs = []

setup(name="pyrobustness",
      version=get_version(),
      description="A simple util library for creating applications which needs to keep running, despite abnormalities",
      author="Šarūnas Navickas",
      author_email="zaibacu@gmail.com",
      license="MIT",
      url="https://github.com/zaibacu/pyRobustness",
      packages=["robust"],
      install_requires=[str(ir.req) for ir in install_reqs],
      test_suite="pytest",
      tests_require=["pytest"])
