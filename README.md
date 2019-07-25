<h1 align="center">
  visma - VISual MAth
</h1>

<h4 align="center">
A math equation solver and visualizer
</h4>

![visma](https://raw.githubusercontent.com/wiki/aerospaceresearch/visma/assets/banner.png)

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

[![PyPI](https://img.shields.io/pypi/v/VISualMAth.svg?style=for-the-badge)](https://pypi.org/project/VISualMAth)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/VISualMAth.svg?style=for-the-badge)](https://pypi.org/project/VISualMAth)

**NOTE:** VISualMAth is supported for python3 and above only. The recommended installation method is through pip/pip3.

- To install do

```shell
$ pip3 install visualmath
```

This sets up the environment to run on your computer.

- For launching **visma** do

```shell
$ visma
>>> gui
```

- For windows user (and those for whom) the above launching option is not available, to launch **visma** do, from here you will be redirected to VisMa interactive shell, which can be used to open GUI or CLI

```shell
mayank@mayank-Lenovo-ideapad-310-15IKB:~$ python3
>>> from visma.main import init
>>> init()
Welcome! This is Visual Maths Interactive Shell...
type 'help' for a User Manual and Ctrl + D to Exit prompt

>>> simplify(2 + x + 11)
INPUT: 2.0 + x + 11.0
OPERATION: simplify
OUTPUT: 13.0 + x

2.0 + x + 11.0

(Adding 11.0 and 2.0)
13.0 + x

>>> 
[5]+  Stopped                 python3

```


## Download:


[![GitHub release](https://img.shields.io/github/release/aerospaceresearch/visma/all.svg?style=for-the-badge)](https://github.com/aerospaceresearch/visma/releases)
[![GitHub repo size in bytes](https://img.shields.io/github/repo-size/aerospaceresearch/visma.svg?style=for-the-badge)](https://github.com/aerospaceresearch/visma/releases)


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

**NOTE:** If using pip instead of pip3 for installing, make sure to check if the pip exists in python3 library by checking the pip version.

```shell
$ pip --version
```

## Docs

[![Github Wiki](https://img.shields.io/badge/wiki-visma-green.svg?style=for-the-badge)](https://github.com/aerospaceresearch/visma/wiki)
![GitHub code size in bytes](https://img.shields.io/github/languages/code-size/aerospaceresearch/visma.svg?style=for-the-badge)

For code documentation and learning how to use **visma** check out the [wiki](https://github.com/aerospaceresearch/visma/wiki).

## Demo

Below are some demos showing visma and its capabilities:
- GUI
![visma](https://raw.githubusercontent.com/wiki/aerospaceresearch/visma/assets/demo.gif)

- CLI
![](/assets/demo-cli.gif)

To see all features of **visma**, check [this](https://github.com/aerospaceresearch/visma/wiki/Features) out.


## Contribute:

[![GitHub pull requests](https://img.shields.io/github/issues-pr/aerospaceresearch/visma.svg?style=for-the-badge)](https://github.com/aerospaceresearch/visma/pulls)
[![GitHub issues](https://img.shields.io/github/issues/aerospaceresearch/visma.svg?style=for-the-badge)](https://github.com/aerospaceresearch/visma/issues)
[![Zulip](https://img.shields.io/badge/Chat-on%20Zulip-17C789.svg?style=for-the-badge)](https://aerospaceresearch.zulipchat.com/#narrow/stream/181873-visma)

PRs are welcomed. For contributing to **visma** refer [CONTRIBUTING.md](https://github.com/aerospaceresearch/visma/blob/master/CONTRIBUTING.md). If there are any issues or ideas they can be addressed through the [issues](https://github.com/aerospaceresearch/visma/issues) or in [chat room](https://aerospaceresearch.zulipchat.com/#narrow/stream/181873-visma).


## License:

[![License: GPL v3](https://img.shields.io/github/license/aerospaceresearch/visma.svg?style=for-the-badge)](https://github.com/aerospaceresearch/visma/blob/master/LICENSE)

**visma** is distributed under the [**GNU GPL-3**](https://github.com/aerospaceresearch/visma/blob/master/LICENSE) or later.
