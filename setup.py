#!/usr/bin/env python
# -*- coding: utf-8 -*-

from distutils.core import setup

setup(
    name='weibo',
    version='0.1.5',
    description='Python sina weibo sdk',
    author='Lx Yu',
    author_email='lixinfish@gmail.com',
    py_modules=['weibo', ],
    package_data={'': ['LICENSE'], },
    url='http://lxyu.github.com/weibo/',
    license=open('LICENSE').read(),
    long_description=open('README.rst').read(),
    install_requires=[
        "requests",
    ],
)
