import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="VISualMAth",
    description="visma - VISual MAth : A math equation solver and visualizer",
    version="0.2.1",
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
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering",
        "Topic :: Scientific/Engineering :: Mathematics",
        "Topic :: Scientific/Engineering :: Visualization",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)"
    ),
    python_requires='>=3',
    install_requires=[
        "PyQt5",
        "matplotlib",
        "numpy"
    ],
    tests_require=[
        "pytest",
        "coverage"
    ]
)
