#!/usr/bin/env python3
"""
Setup script for P2P Privacy Communications
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="p2p-privacy-comm",
    version="1.0.0",
    author="P2P Communications Developer",
    description="A secure peer-to-peer communications program with voice calling, messaging, and link sharing",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/p2p-privacy-comm",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Communications :: Chat",
        "Topic :: Security :: Cryptography",
        "Topic :: System :: Networking",
    ],
    python_requires=">=3.7",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "p2p-comm=main:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
)

