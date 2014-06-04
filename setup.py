#!/usr/bin/env python
# -*- coding: utf-8 -*-

from distutils.core import setup

setup(
    name='weibo',
    version='0.2.0',
    description='Python sina weibo sdk',
    author='Lx Yu',
    author_email='github@lxyu.net',
    py_modules=['weibo', ],
    package_data={'': ['LICENSE'], },
    url='http://lxyu.github.io/weibo/',
    license="BSD",
    long_description=open('README.rst').read(),
    install_requires=[
        "requests",
    ],
)
