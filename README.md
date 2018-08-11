<h1 align="center">
  visma - VISual MAth
</h1>

<h4 align="center">
A math equation solver and visualizer
</h4>

![visma](https://github.com/aerospaceresearch/visma/tree/master/assets/banner.png)

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

**NOTE:** VISualMAth is supported for python3 and above only

The recommended installation method is through pip/pip3. To install do

```shell
$ pip3 install VISualMAth
```

This sets up the environment to run on your computer.

For launching visma do

```shell
$ visma
```

**Note:** For windowss user (and those for whom) the above launching option is not available, to launch visma GUI do

```shell
$ python3
>>> from visma.main import initGUI
>>> initGUI()
```

## Download:

If visma is to be installed locally or for development, download the source zip.

For installing dependencies use the following:

```shell
$ pip3 install -r requirements.txt
```

For launching do

```shell
$ python3 main.py
```

![Github All Releases](https://img.shields.io/github/downloads/aerospaceresearch/visma/total.svg?style=for-the-badge)
![GitHub repo size in bytes](https://img.shields.io/github/repo-size/aerospaceresearch/visma.svg?style=for-the-badge)


**NOTE:** If using pip instead of pip3 for installing, make sure to check if the pip exists in python3 library by checking the pip version.

```shell
$ pip --version
```


## Demo

![visma](https://github.com/aerospaceresearch/visma/tree/master/assets/demo.gif)


## Contribute:

[![GitHub pull requests](https://img.shields.io/github/issues-pr/aerospaceresearch/visma.svg?style=for-the-badge)](https://github.com/aerospaceresearch/visma/pulls)
[![GitHub issues](https://img.shields.io/github/issues/aerospaceresearch/visma.svg?style=for-the-badge)](https://github.com/aerospaceresearch/visma/issues)

## License:
[![License: GPL v3](https://img.shields.io/github/license/aerospaceresearch/visma.svg?style=for-the-badge)](https://github.com/aerospaceresearch/visma/blob/master/LICENSE)
