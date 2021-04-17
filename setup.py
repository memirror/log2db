# -*- coding: utf-8 -*-
# @Author: xiaodong
# @Date  : 2021/4/17

from setuptools import setup, find_packages


def long_description():
    with open("README.md", encoding="utf-8") as file:
        description = file.read()
    return description


with open("requirements.txt") as file:
    requirements = [
        obj.strip() for obj in file.readlines() if obj.strip()
    ]

setup(
    name="log2db",
    version="0.0.1",
    description="logging to database with no block suport by mq and sqlalchemy",
    long_description=long_description(),
    url="https://github.com/xiaodongxiexie/log2db",
    author="xiaodong",
    author_email="xiaodongliang@outlook.com",
    package_data={
        "": [
            "requirements.txt",
        ],
    },
    packages=find_packages(),
    include_package_data=True,
    install_requires=requirements,
    zip_safe=False,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Topic :: Utilities",
    ],
    keywords="logging database mq redis sqlalchemy",
)
  
