#!/usr/bin/env python3
from setuptools import setup, find_packages

setup(
    name="colab-cli",
    version="0.1.0",
    packages=find_packages(),
    py_modules=["colab_cli"],
    install_requires=[
        "requests>=2.25.0",
    ],
    entry_points={
        "console_scripts": [
            "colab-cli=colab_cli:main",
        ],
    },
    author="Jack5316",
    author_email="your.email@example.com",  # Replace with your email
    description="Command-line interface for Google Colab notebooks",
    keywords="colab, jupyter, notebook, cli",
    url="https://github.com/Jack5316/colab-cli",  # Replace with your repo URL if applicable
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    python_requires=">=3.6",
)