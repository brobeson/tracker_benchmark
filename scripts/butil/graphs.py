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


def draw_overlap(scores, tracker_colors, forced_tracker=None):
    """Draw all the overlap graphs.

    Args:
        scores: The score data to graph. This is a 2D array of data. Each row
            corresponds to one tracker. Each column corresponds to one tracking
            attribute, with an additional column for ALL. Each entry in the
            array is a scripts.model.score.Score object.
            [
                [ Score, Score, Score, ..., Score ]  # tracker 1
                [ Score, Score, Score, ..., Score ]  # tracker 2
                ...
                [ Score, Score, Score, ..., Score ]  # tracker N
            ]

    Returns:
        Nothing

    Raises:
        Nothing
    """
    figures = []
    if not os.path.exists("graphs"):
        os.mkdir("graphs")
    for a in range(len(scores[0])):
        print("Graphing", scores[0][a].name)
        attribute_scores = []
        for tracker in scores:
            attribute_scores.append(tracker[a])
        figure = _draw_overlap_graph(
            attribute_scores, tracker_colors, forced_tracker
        )
        figure.savefig(
            os.path.join("graphs", f"{attribute_scores[0].name}.svg"),
            bbox_inches="tight",
        )
        figures.append(figure)
    plt.show()


def _draw_overlap_graph(scores, tracker_colors, forced_tracker):
    scores = sorted(
        scores, key=lambda score: sum(score.successRateList), reverse=True
    )
    figure = plt.figure(figsize=(9, 6))
    axes = _make_axes(figure, scores[0].name)
    a = 0
    b = min([config.MAXIMUM_LINES, len(scores)])
    for score in enumerate(scores[a:b]):
        _graph_data(
            axes,
            score[1].successRateList,
            {
                "color": tracker_colors[score[1].tracker]["color"],
                "name": score[1].tracker,
                "rank": score[0] + 1,
                "line style": tracker_colors[score[1].tracker]["style"],
                "opacity": 1.0 if score[1].tracker == forced_tracker else 0.25
            },
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


def _make_axes(figure, title):
    axes = figure.add_subplot(1, 1, 1)
    axes.set_title(f"OPE - {title}", {"fontsize": "medium"})
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
    return axes


def _graph_data(axes, data, style):
    mean = sum(data) / len(data)
    x, y = _smooth_data(config.thresholdSetOverlap, data)
    axes.plot(
        x,
        y,
        color=style["color"],
        label=f"{style['rank']} - {style['name']} [{mean:.2f}]",
        linewidth=1.0,
        linestyle=style["line style"],
        alpha=style["opacity"],
    )
