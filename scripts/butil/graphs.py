"""Utility functions for drawing overlap and precision graphs."""

import os
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import make_interp_spline
import config


def get_color_table(trackers):
    """Generate a table of colors for graph lines, indexed by tracker name.

    Parameters:
    trackers: A list of strings. Each string is the name of a tracker.
    Returns: A dictionary mapping each tracker to a unique color.
    """
    line_styles = ["-", "--", "-.", ":"]
    curve_styles = []
    for style in line_styles:
        for color in config.LINE_COLORS:
            curve_styles.append({"color": color, "style": style})
    lut = {}
    for tracker in enumerate(trackers):
        lut[tracker[1]] = curve_styles[tracker[0]]
    return lut


def draw_overlap(scores, tracker_colors):
    """Draw all the overlap graphs.

    Parameters:
    scores (list): A list of of lists of Score objects.
    [ tracker 1, tracker 2, ..., tracker n ]
       [ attr 1 score, attr 2 score, ..., attr m score ]
    """
    figures = []
    if not os.path.exists("graphs"):
        os.mkdir("graphs")
    for a in range(len(scores[0])):
        attribute_scores = []
        for tracker in scores:
            attribute_scores.append(tracker[a])
        figure = _draw_overlap_graph(attribute_scores, tracker_colors)
        figure.savefig(
            os.path.join("graphs", f"{attribute_scores[0].name}.svg"),
            bbox_inches="tight",
        )
        figures.append(figure)
    plt.show()


def _draw_overlap_graph(scores, tracker_colors):
    scores = sorted(
        scores, key=lambda score: sum(score.successRateList), reverse=True
    )
    figure = plt.figure(figsize=(9, 6))
    axes = figure.add_subplot(1, 1, 1)
    axes.set_title(f"OPE - {scores[0].name}", {"fontsize": "medium"})
    axes.autoscale(enable=True, axis="both", tight=True)
    axes.set_xlabel("Thresholds")
    axes.grid(
        b=True,
        which="major",
        axis="both",
        color="#101010",
        alpha=0.5,
        linestyle=":",
    )
    num_lines = min([config.MAXIMUM_LINES, len(scores)])
    for score in scores[0 : num_lines - 1]:
        mean = sum(score.successRateList) / len(score.successRateList)
        x, y = _smooth_data(config.thresholdSetOverlap, score.successRateList)
        axes.plot(
            x,
            y,
            color=tracker_colors[score.tracker]["color"],
            label=f"{score.tracker} [{mean:.2f}]",
            linewidth=1.0,
            linestyle=tracker_colors[score.tracker]["style"],
        )
    axes.legend()  # This must remain after the axes.plot() calls.
    return figure


def _smooth_data(x, y):
    # Adapted from
    # https://stackoverflow.com/questions/5283649/plot-smooth-line-with-pyplot
    # I can improve on it later.
    new_x = np.linspace(min(x), max(x), 300)
    spline = make_interp_spline(x, y, 3)
    return new_x, spline(new_x)
