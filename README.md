[![PyPI version](https://badge.fury.io/py/arblay.svg)](https://badge.fury.io/py/arblay)
[![Downloads](https://pepy.tech/badge/arblay)](https://pepy.tech/project/arblay)
[![GitHub license](https://img.shields.io/github/license/YoshikiKubotani/arbitrary_mpl_figures)](https://github.com/YoshikiKubotani/arbitrary_mpl_figures/blob/master/LICENSE)

# arblay

<img src="https://raw.githubusercontent.com/YoshikiKubotani/arbitrary_mpl_figures/master/resources/0_readme.png">

This repository stores a source code for the `arblay` library.  `arblay` is a small unofficial extension of [matplotlib](https://github.com/matplotlib/matplotlib), which aims at making matplotlib figures with arbitrary layouts.  You can easily generate a variety of figures specifying each Axes object size in pixel.

Note: This repository only deals with rectangle-shaped figures having rectangle-shaped Axes with no rotation.  You cannot make any warped figures (i.e. rounds, trapezia, and triangles) and ones with tilting Axes.

# Install

Run the following code.

```
pip install arblay
```

# How to Use

See description in [instruction.md](/resources/instruction.md).

You can try to generate some examples from [demo.ipynb](/demo.ipynb) as well.