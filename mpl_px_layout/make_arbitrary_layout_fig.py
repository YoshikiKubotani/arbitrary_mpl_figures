from typing import Sequence, Iterable, Mapping, Collection, List, Any, Dict, Union, Tuple, Optional

import numpy as np
from itertools import accumulate, chain

from matplotlib.figure import Figure
from matplotlib.axes import Axes
from mpl_toolkits.axes_grid1 import Divider, Size
import matplotlib.pyplot as plt

import logging

def _count_used_and_skipped_tiles(
    curr_pos: int,
    tile_base: Sequence[int],
    ax_length_px: int,
    margin_length_px: int,
    logger: logging.Logger
    ) -> Tuple[int, Tuple[int, int]]:
    """Count how many tiles are used for Axes objects and the margins between them.

    Parameters
    ----------
    curr_pos : int
        The index indicating from which tile the current Axes object starts.
    tile_base : Sequence[int]
        The sequence object containing the length of each tile.
    ax_length_px : int
        The pixel length of the current Axes object.
    margin_length_px : int
        The pixel length of the margin next the current Axes object.
    logger: logging.Logger
        A Python logger object with one stream handler. Outputs log messages to the console based on the specified level.

    Returns
    -------
    next_pos: int
        The index indicating from which tile the next Axes object starts.
    n_range: Tuple[int]
        The tuple of two indexes indicating from and to which tile the current Axes objects occupy.
    """
    # Calculate how many tiles are used to make one Axes object.
    logger.debug("### Tile ###")
    logger.debug("curr_ax: {:5d}".format(ax_length_px))
    used_tile = 0
    tile_start = curr_pos
    # Count the number of tiles needed to reach a specified length.
    for tile_id, accum_tile in enumerate(accumulate(tile_base[tile_start:])):
        if accum_tile < ax_length_px:
            continue
        elif accum_tile == ax_length_px:
            used_tile = tile_id + 1
        logger.debug("Looped to index={:5d} in {}".format(tile_id, tile_base[tile_start:]))
        break

    # Calculate how many tiles are used to make a margin between two Axes objects.
    logger.debug("### Margin ###")
    logger.debug("next_margin: {: 5d}".format(margin_length_px))
    skip_tile = 0
    margin_start = curr_pos + used_tile
    # Margins can be minus values.
    if margin_length_px < 0:
        margin_iterator = accumulate(reversed(tile_base[:margin_start]))
        just_for_print = list(reversed(tile_base[:margin_start]))
        reverse = True
    else:
        margin_iterator = accumulate(tile_base[margin_start:])
        just_for_print = tile_base[margin_start:]
        reverse = False
    # Count the number of tiles needed to reach a specified length.
    for margin_id, accum_tile in enumerate(margin_iterator):
        if accum_tile < abs(margin_length_px):
            continue
        elif accum_tile == abs(margin_length_px):
            skip_tile = -(margin_id + 1) if reverse else margin_id + 1
        logger.debug("Looped to index={:5d} in {}".format(margin_id, just_for_print))
        break

    n_range = (tile_start, tile_start + used_tile)
    next_pos = curr_pos + used_tile + skip_tile

    logger.debug("{:^8s} -> {:^8s}(= {:^9s} + {:^9s} + {:^9s})".format("curr_pos", "next_pos", "curr_pos", "used_tile", "skip_tile"))
    logger.debug("{:^8s} -> {:^8s}(= {:^9s} + {:^9s} + {:^9s})\n".format(str(curr_pos), str(next_pos), str(curr_pos), str(used_tile), str(skip_tile)))

    return next_pos, n_range


def make_fixed_pixel_size_axes(
    fig_dpi: int,
    ax_w_px: Sequence[Sequence[int]],
    ax_h_px: Sequence[Sequence[int]],
    ax_w_margin_px: Sequence[Sequence[int]],
    ax_h_margin_px: Sequence[Sequence[int]],
    off_index: Sequence[Tuple[int, int]],
    fig_margin_inch: Collection[float]=(0.5, 0.5, 0.5, 0.5),
    preview: bool=False,
    verbose: bool=False,
    ) -> Tuple[List[Axes], Figure]:
    """Make the matplotlib figure with an arbitrary number of axes aligned in an arbitrary layout.

    Generate a matplotlib Figure object of arbitrary size with multiple Axes objects. The size of the Figure is specified by the dpi (dots per inch),
    the margin from the edge to the drawing area, the width and height occupied by each Axes object, and the margins between these Axes in pixels
    Read README.md for instructions on how to determine specific arguments.

    Parameters
    ----------
    fig_dpi : int
        The number of dots per inch of figures to create.
    ax_w_px : Sequence[Sequence[int]]
        A list specifying the width in pixels of the axes in the figure to create.
    ax_h_px : Sequence[Sequence[int]]
        A list specifying the height in pixels of the axes in the figure to create.
    ax_w_margin_px : Sequence[Sequence[int]]
        A list specifying the width in pixels of the margins in the figure to create.
    ax_h_margin_px : Sequence[Sequence[int]]
        A list specifying the height in pixels of the margins between axes in the figure to create.
    off_index : Sequence[Tuple[int, int]]
        A list of indexes of the Axes objects not to be drawn.  The index is based on the lower-left corner of the figure, and increases
        as it goes up for rows and right for columns.  Note that each index is specified in (column, row) order.
    fig_margin_inch : Collection[float], optional
        A tuple specifying the edge margins of a figure in inches in the order (left, top, right, bottom). (The default is (0.5, 0.5, 0.5, 0.5).)
    preview : bool, optional
        The flag of whether to visualize the preview of the figure or not. (The default is False, which implies not visualizing it.)
    verbose : bool, optional
        The flag of whether to print the detailed logging message or not. (The default is False, which implies not printing messages.)

    Returns
    -------
    axes_list : List[Axes]
        A list of created axes.
    fig : Figure
        A figure where the created axes are placed.

    Raises
    ------
    ValueError
        Raise an error if the length of the input lists is incorrect, or the invalid type values are specified.  Refer to the error sentence
        for detailed instructions.
    """
    # Initialize the logger object.
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    console_handler = logging.StreamHandler()
    formatter = logging.Formatter("[%(levelname)s] - %(message)s")
    if verbose:
        console_handler.setLevel(logging.DEBUG)
    else:
        console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # Catch error messages.
    try:
        # The empty list is not allowed for the sequence containing widths or heights of the Axes objects.
        if len(ax_w_px) == 0 or len(ax_h_px) == 0:
            raise ValueError("The empty list is NOT allowed for the sequence containing widths or heights of the Axes objects.")
        # All the sequence in the sequence containing widths or heights of the Axes objects should not be empty.
        if any([len(each_ax_w_px) == 0 for each_ax_w_px in ax_w_px]) or any([len(each_ax_h_px) == 0 for each_ax_h_px in ax_h_px]):
            raise ValueError("All the sequence in the sequence containing widths or heights of the Axes objects should NOT be empty.")
        # Both the length of the sequence containing widths or heights of the Axes objects and that of the sequence containing margins should be the same.
        if len(ax_w_px) != len(ax_w_margin_px):
            raise ValueError(
                "The number of rows in the sequence containing the width (i.e. len(ax_w_px) ) and the sequence containing its margin (i.e. len(ax_w_margin_px) ) \
                must be the same, but they do not match because the former is {:2d} and the latter is {:2d}.".format(len(ax_w_px), len(ax_w_margin_px))
            )
        if len(ax_h_px) != len(ax_h_margin_px):
            raise ValueError(
                "The number of columns in the sequence containing the height (i.e. len(ax_h_px) ) and the sequence containing its margin (i.e. len(ax_h_margin_px) ) \
                must be the same, but they do not match because the former is {:2d} and the latter is {:2d}.".format(len(ax_h_px), len(ax_h_margin_px))
            )
        # The length of each margin sequence should be -1 of that of the corresponding sequence containing widths or heights of the Axes objects.
        if any([len(each_ax_w_px)-1 != len(each_ax_w_margin_px) for each_ax_w_px, each_ax_w_margin_px in zip(ax_w_px, ax_w_margin_px)]) \
            or any([len(each_ax_h_px)-1 != len(each_ax_h_margin_px) for each_ax_h_px, each_ax_h_margin_px in zip(ax_h_px, ax_h_margin_px)]):
            raise ValueError("The length of each margin sequence should be -1 of that of the corresponding sequence containing widths or heights of the Axes objects.")
        # Each index specified in the `off_index` argument must be a tuple.
        if any([not isinstance(each_index, tuple) for each_index in off_index]):
            raise ValueError("Each index specified in the `off_index` argument must be a tuple.")
    except ValueError as e:
        logger.error(e)

    num_column = len(ax_h_px)
    num_row = len(ax_w_px)

    # Get the area occupied by the Axes objects in pixel.
    axes_w_px = max([sum(each_ax_w_px) + sum(each_ax_w_margin_px) for each_ax_w_px, each_ax_w_margin_px in zip(ax_w_px, ax_w_margin_px)])
    axes_h_px = max([sum(each_ax_h_px) + sum(each_ax_h_margin_px) for each_ax_h_px, each_ax_h_margin_px in zip(ax_h_px, ax_h_margin_px)])

    # Convert pixels to inches and get the figure size in inches.
    axes_w_inch = axes_w_px / fig_dpi
    axes_h_inch = axes_h_px / fig_dpi
    fig_w_inch = axes_w_inch + fig_margin_inch[0] + fig_margin_inch[2]
    fig_h_inch = axes_h_inch + fig_margin_inch[1] + fig_margin_inch[3]

    # Align the Axes objects and their margins in the correct order (i.e. left to right for width and bottom to top for height), and get the list of accumulated lengths each.
    accum_ax_w_px = [list(accumulate(list(chain.from_iterable(zip(each_ax_w_px, each_ax_w_margin_px+[0]))))) for each_ax_w_px, each_ax_w_margin_px in zip(ax_w_px, ax_w_margin_px)]
    accum_ax_h_px = [list(accumulate(list(chain.from_iterable(zip(each_ax_h_px, each_ax_h_margin_px+[0]))))) for each_ax_h_px, each_ax_h_margin_px in zip(ax_h_px, ax_h_margin_px)]

    # Since the accumulated length list above contains the same numbers when the original length of margins or Axes objects have 0, remove those numbers and sort them.
    accum_tile_w_px = np.sort(np.unique(np.append(0, np.array(accum_ax_w_px))))
    tile_w_base = (accum_tile_w_px[1:] - accum_tile_w_px[:-1]).tolist()
    accum_tile_h_px = np.sort(np.unique(np.append(0, np.array(accum_ax_h_px))))
    tile_h_base = (accum_tile_h_px[1:] - accum_tile_h_px[:-1]).tolist()

    # Make the vertical and horizontal constraints for the Divider object.  These values imply the length of the tiles to construct the Axes object and its margins.
    tile_w_for_divider = [Size.Fixed(fig_margin_inch[0])] + [Size.Fixed(each_tile_w/fig_dpi) for each_tile_w in tile_w_base]
    tile_h_for_divider = [Size.Fixed(fig_margin_inch[1])] + [Size.Fixed(each_tile_h/fig_dpi) for each_tile_h in tile_h_base]
    # Store these values in a list also in a standard python float format for logging and other processes.
    tile_w_base = [0]+tile_w_base
    tile_h_base = [0]+tile_h_base
    logger.debug("tile_w: {}".format(tile_w_base))
    logger.debug("tile_h: {}\n".format(tile_h_base))

    fig = plt.figure(dpi=fig_dpi, figsize=(fig_w_inch, fig_h_inch))
    # The rect parameter will be ignored as set_axes_locator is used.
    dummy_rect = (0.0, 0.0, 1.0, 1.0)

    # Initialize the Divider object that keeps the vertical and horizontal sizes on which the division will be based.
    # See also https://matplotlib.org/stable/tutorials/toolkits/axes_grid.html#axesdivider.
    divider = Divider(fig, dummy_rect, tile_w_for_divider, tile_h_for_divider, aspect=False)

    axes_list = []
    # For each row, store a list of indices, each of which indicates from which tile the current Axes object starts.
    curr_ax_part_w_pos = [1 for _ in range(num_row)]
    # For each column, store a list of indices, each of which indicates from which tile the current Axes object starts.
    curr_ax_part_h_pos = [1 for _ in range(num_column)]
    for row_id in range(num_row):
        for column_id in range(num_column):
            logger.debug("####### (row, column) = ({}, {}) ############################".format(row_id, column_id))
            curr_ax_w_px = ax_w_px[row_id][column_id]
            curr_ax_h_px = ax_h_px[column_id][row_id]
            is_empty_box = curr_ax_w_px == 0 or curr_ax_h_px == 0
            try:
                next_ax_w_margin_px = ax_w_margin_px[row_id][column_id]
            except IndexError:
                next_ax_w_margin_px = 0
            try:
                next_ax_h_margin_px = ax_h_margin_px[column_id][row_id]
            except IndexError:
                next_ax_h_margin_px = 0

            logger.debug("### width ###########")
            curr_ax_part_w_pos[row_id], nx_range = _count_used_and_skipped_tiles(
                curr_pos=curr_ax_part_w_pos[row_id],
                tile_base=tile_w_base,
                ax_length_px=curr_ax_w_px,
                margin_length_px=next_ax_w_margin_px,
                logger=logger
            )

            logger.debug("### height ###########")
            curr_ax_part_h_pos[column_id], ny_range = _count_used_and_skipped_tiles(
                curr_pos=curr_ax_part_h_pos[column_id],
                tile_base=tile_h_base,
                ax_length_px=curr_ax_h_px,
                margin_length_px=next_ax_h_margin_px,
                logger=logger
            )

            # If the index of the focused Axes object is specified in the off_index or its length is zero, the function skips that Axes object.
            skip_flag = any([(column_id, row_id) == each_index for each_index in off_index])  or is_empty_box
            if skip_flag:
                continue

            # Put the Axes object in a correct place of a figure.
            ax = Axes(fig, divider.get_position())
            ax.set_axes_locator(divider.new_locator(nx=nx_range[0], nx1=nx_range[1], ny=ny_range[0], ny1=ny_range[1]))

            # Preview the figure.
            if preview:
                ax.tick_params(bottom=False, labelbottom=False, left=False, labelleft=False)
                fig.show()
            axes_list.append(ax)

            fig.add_axes(ax)
    # Reset the logger object not to prevent its configuration from persisting.
    logger.removeHandler(console_handler)
    console_handler.close()

    return axes_list, fig