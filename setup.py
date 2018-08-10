import setuptools
import pip
try:
    from pip._internal.utils.misc import get_installed_distributions
except ImportError:  # pip < 10
    from pip import get_installed_distributions

with open("README.md", "r") as fh:
    long_description = fh.read()
packages = [package.project_name for package in get_installed_distributions()]

requirements = ['PyQt5', 'matplotlib', 'numpy', 'coverage', 'pytest']
for requirement in requirements:
    if requirement not in packages:
        pip.main(['install', '--user', requirement])

setuptools.setup(
    name="VISualMAth",
    description="visma - VISual MAth : A math equation solver and visualizer",
    version="0.2.0",
    author="Siddharth Kothiyal, Shantanu Mishra",
    author_email="sid.kothiyal27@gmail.com, 8hantanu@gmail.com",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/aerospaceresearch/visma",
    project_urls={
        'Documentation': 'https://github.com/aerospaceresearch/visma/wiki',
        'Source': 'https://github.com/aerospaceresearch/visma',
        'Issues': 'https://github.com/aerospaceresearch/visma/issues',
        'Chat': 'https://gitter.im/aerospaceresearch/visma'
    },
    packages=setuptools.find_packages(),
    scripts=['bin/visma'],
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering",
        "Topic :: Scientific/Engineering :: Mathematics",
        "Topic :: Scientific/Engineering :: Visualization"
    ),
    python_requires='>=3'
)
