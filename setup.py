# Author: Yoshiki Kubotani <yoshikikubotani.lab@gmail.com>
# Copyright 2022 Yoshiki Kubotani
# License: MIT

from setuptools import setup
import mpl_px_layout

DESCRIPTION = "Making the matplotlib figures with an arbitrary layout specifying pixels"
NAME = 'mpl_px_layout'
AUTHOR = 'Yoshiki Kubotani'
AUTHOR_EMAIL = 'yoshikikubotani.lab@gmail.com'
URL = 'https://github.com/YoshikiKubotani/arbitrary_mpl_figures'
LICENSE = 'MIT'
DOWNLOAD_URL = 'https://github.com/YoshikiKubotani/arbitrary_mpl_figures'
VERSION = mpl_px_layout.__version__
PYTHON_REQUIRES = ">=3.6"

INSTALL_REQUIRES = [
    'matplotlib>=3.3.4',
    'seaborn>=0.11.0',
    'numpy >=1.20.3',
    'pandas>=1.2.4',
    'matplotlib>=3.3.4',
    'scipy>=1.6.3',
    'scikit-learn>=0.24.2',
]

PACKAGES = [
    'mpl_px_layout'
]

CLASSIFIERS = [
    'Intended Audience :: Science/Research',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
    'Programming Language :: Python :: 3 :: Only',
    'Topic :: Scientific/Engineering',
    'Topic :: Scientific/Engineering :: Visualization',
    'Topic :: Scientific/Engineering :: Artificial Intelligence',
    'Topic :: Multimedia :: Graphics',
    'Framework :: Matplotlib',
]

with open('README.md', 'r', encoding='utf-8') as fp:
    readme = fp.read()
long_description = readme

setup(name=NAME,
      author=AUTHOR,
      author_email=AUTHOR_EMAIL,
      maintainer=AUTHOR,
      maintainer_email=AUTHOR_EMAIL,
      description=DESCRIPTION,
      long_description=long_description,
      long_description_content_type="text/markdown",
      license=LICENSE,
      url=URL,
      version=VERSION,
      download_url=DOWNLOAD_URL,
      python_requires=PYTHON_REQUIRES,
      install_requires=INSTALL_REQUIRES,
      packages=PACKAGES,
      classifiers=CLASSIFIERS
    )