#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from setuptools import setup

setup(
    name='oneesama',
    packages=[
        'oneesama',
        'imouto',
    ],
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'oneesama = oneesama:main',
        ],
    },
    install_requires=[
        'flask',
        'flask_peewee',
    ],
    setup_requires=[
        'pytest-runner',
    ],
    tests_requires=[
        'pytest',
    ],
)
