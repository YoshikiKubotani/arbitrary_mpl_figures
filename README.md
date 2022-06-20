# mpl_px_layout

<img src="https://raw.githubusercontent.com/YoshikiKubotani/arbitrary_mpl_figures/master/resources/0_readme.png">

This repository stores a source code for the `mpl_px_layout` library.  `mpl_px_layout` is a small unofficial extension of [matplotlib](https://github.com/matplotlib/matplotlib), which aims at making matplotlib figures with arbitrary layouts.  You can easily generate a variety of figures specifying each Axes object size in pixel.

Note: This repository only deals with rectangle-shaped figures having rectangle-shaped Axes with no rotation.  You cannot make any warped figures (i.e. rounds, trapezia, and triangles) and ones with tilting Axes.

# Install

Run the following code.

```
pip install mpl_px_layout
```

# How to Use

See description in [instruction.md](/resources/instruction.md).

You can try to generate some examples from [demo.ipynb](/demo.ipynb) as well.