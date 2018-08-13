<h1 align="center">
  visma - VISual MAth
</h1>

<h4 align="center">
A math equation solver and visualizer
</h4>

![visma](https://github.com/aerospaceresearch/visma/raw/master/assets/banner.png)

<p align="center">
  <a href="https://travis-ci.org/aerospaceresearch/visma">
    <img alt="Build Status" src="https://img.shields.io/travis/aerospaceresearch/visma.svg?style=for-the-badge">
  </a>
  <a href="https://www.codacy.com/app/aerospaceresearch/visma">
    <img alt="Codacy Badge" src="https://img.shields.io/codacy/grade/bed991e6ae14471d858c0890510ca8d2.svg?style=for-the-badge">
  </a>
  <a href="https://coveralls.io/github/aerospaceresearch/visma">
    <img alt="Coveralls Coverage" src="https://img.shields.io/coveralls/github/aerospaceresearch/visma.svg?style=for-the-badge">
  </a>
</p>


An equation solver and visualizer, which aims to help in grasping how mathematical equations are transformed and solved. By this the threshold for obtaining deeper mathematical understanding can be reduced.


## Installation

**NOTE:** VISualMAth is supported for python3 and above only. The recommended installation method is through pip/pip3.

[![PyPI](https://img.shields.io/pypi/v/VISualMAth.svg?style=for-the-badge)](https://pypi.org/project/VISualMAth)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/VISualMAth.svg?style=for-the-badge)](https://pypi.org/project/VISualMAth)

- To install do

```shell
$ pip3 install VISualMAth
```

This sets up the environment to run on your computer.

- For launching **visma** do

```shell
$ visma
```

**Note:** For windows user (and those for whom) the above launching option is not available, to launch **visma** GUI do

```shell
$ python3
>>> from visma.main import initGUI
>>> initGUI()
```
For more about installation look into [Install wiki](https://github.com/aerospaceresearch/visma/wiki/Install).

## Download:

If **visma** is to be installed locally or for development:

- Download the [source zip](https://github.com/aerospaceresearch/visma/archive/master.zip) and extract.
- For installing dependencies, from source folder do

```shell
$ pip3 install -r requirements.txt
```

- For launching do

```shell
$ python3 main.py
```

[![Github All Releases](https://img.shields.io/github/downloads/aerospaceresearch/visma/total.svg?style=for-the-badge)](https://github.com/aerospaceresearch/visma/releases)
![GitHub code size in bytes](https://img.shields.io/github/languages/code-size/aerospaceresearch/visma.svg?style=for-the-badge)

**NOTE:** If using pip instead of pip3 for installing, make sure to check if the pip exists in python3 library by checking the pip version.

```shell
$ pip --version
```

## Docs

For learning how to use **visma** and code documentation check out the [wiki](https://github.com/aerospaceresearch/visma/wiki).

[![Github Wiki](https://img.shields.io/badge/wiki-visma-blue.svg?style=for-the-badge)](https://github.com/aerospaceresearch/visma/wiki)

Below is a quick demo of using **visma** and some of its capabilities.


## Demo

![visma](https://github.com/aerospaceresearch/visma/raw/master/assets/demo.gif)

To see all features of **visma**, check [this](https://github.com/aerospaceresearch/visma/wiki/Features) out.


## Contribute:

PRs are welcomed. For contributing to **visma** refer the [Dev Manual](https://github.com/aerospaceresearch/visma/wiki/DevMan). If there are any issues or ideas they can be addressed through the [issues](https://github.com/aerospaceresearch/visma/issues) or in [chat room](https://gitter.im/aerospaceresearch/visma).

[![GitHub pull requests](https://img.shields.io/github/issues-pr/aerospaceresearch/visma.svg?style=for-the-badge)](https://github.com/aerospaceresearch/visma/pulls)
[![GitHub issues](https://img.shields.io/github/issues/aerospaceresearch/visma.svg?style=for-the-badge)](https://github.com/aerospaceresearch/visma/issues)
[![Gitter](https://img.shields.io/gitter/room/aerospaceresearch/visma.svg?style=for-the-badge)](https://gitter.im/aerospaceresearch/visma)


## License:

**visma** is distributed under the [**GNU GPL-3**](https://github.com/aerospaceresearch/visma/blob/master/LICENSE) or later.

[![License: GPL v3](https://img.shields.io/github/license/aerospaceresearch/visma.svg?style=for-the-badge)](https://github.com/aerospaceresearch/visma/blob/master/LICENSE)
