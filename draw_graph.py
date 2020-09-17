"""Draw results graphs."""

import argparse
import os
import sys
import matplotlib.pyplot as plt
import config
from scripts.butil import load_results, graphs


def main():
    """The main entry point for the script."""
    arguments = _parse_command_line()
    trackers = _load_trackers(config.RESULT_SRC.format(arguments.evaluation_type))
    tracker_colors = graphs.get_color_table(trackers)
    score_list = _load_scores(trackers, arguments.evaluation_type, arguments.test_name)
    if arguments.graph_type == "precision":
        graph = get_precision_graph(
            score_list, arguments.evaluation_type, arguments.test_name
        )
    else:
        graph = get_overlap_graph(
            score_list, arguments.evaluation_type, arguments.test_name, tracker_colors
        )
    graph.show()


def _parse_command_line() -> argparse.Namespace:
    """
    Parse the command line arguments.

    :return: The parsed command line arguments.
    :rtype: argparse.Namespace
    """
    parser = argparse.ArgumentParser(
        description="Draw overlap success or center error precision graphs.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "--evaluation-type",
        help="The type of evaluation to graph.",
        choices=["OPE", "SRE", "TRE"],
        default="OPE",
    )
    parser.add_argument(
        "test_name",
        help="The name of the test to graph. This should match a name that you used when you ran "
        "the run_trackers.py script.",
    )
    parser.add_argument(
        "graph_type",
        choices=["overlap", "precision"],
        help="The type of graphs to draw: overlap success or center error precision.",
    )
    return parser.parse_args()


def _load_trackers(results_directory: str):
    """
    Load the list of the trackers available to graph.

    :param str results_directory: The directory that contains the tracking results. This directory
        is read to get the available trackers.
    :return: The list of available trackers.
    :rtype: list
    """
    trackers = os.listdir(results_directory)
    return sorted(trackers)


def _load_scores(trackers, evaluation_type, test_name):
    score_list = []
    for tracker in trackers:
        score_list.append(load_results.load_scores(evaluation_type, tracker, test_name))
    return score_list


def get_overlap_graph(score_list, evalType, testname, tracker_colors):
    """Generate the overlap success graph."""
    graphs.draw_overlap(score_list, tracker_colors, "dmdnet")
    sys.exit(0)
    plt.figure(figsize=(9, 6), dpi=70)
    rankList = sorted(score_list, key=lambda o: sum(o[0].successRateList), reverse=True)
    for i, result in enumerate(rankList):
        result = rankList[i]
        tracker = result[0].tracker
        attr = result[0]
        if len(attr.successRateList) == len(config.thresholdSetOverlap):
            if i < config.MAXIMUM_LINES:
                ls = "-"
                if i % 2 == 1:
                    ls = "--"
                ave = sum(attr.successRateList) / float(len(attr.successRateList))
                plt.plot(
                    config.thresholdSetOverlap,
                    attr.successRateList,
                    c=config.LINE_COLORS[i],
                    label="{0} [{1:.2f}]".format(tracker, ave),
                    lw=2.0,
                    ls=ls,
                )
            # else:
            #    plt.plot(config.thresholdSetOverlap, attr.successRateList,
            #        label='', alpha=0.5, c='#202020', ls='--')
        else:
            print("err")
    plt.title("{0}_{1} (sequence average)".format(evalType, testname.upper()))
    plt.rcParams.update({"axes.titlesize": "medium"})
    plt.xlabel("Thresholds")
    plt.autoscale(enable=True, axis="x", tight=True)
    plt.autoscale(enable=True, axis="y", tight=True)
    plt.grid(color="#101010", alpha=0.5, ls=":")
    plt.legend(fontsize="medium")
    # plt.savefig(BENCHMARK_SRC + 'graph/{0}_sq.png'.format(evalType), dpi=74, bbox_inches='tight')
    plt.show()
    return plt


def get_precision_graph(score_list, evalType, testname):
    """Generate a center precision error graph."""
    plt.figure(figsize=(9, 6), dpi=70)
    rankList = sorted(score_list, key=lambda o: o[0].precisionList[20], reverse=True)
    for i, result in enumerate(rankList):
        result = rankList[i]
        tracker = result[0].tracker
        attr = result[0]
        if len(attr.precisionList) == len(config.thresholdSetError):
            if i < config.MAXIMUM_LINES:
                ls = "-"
                if i % 2 == 1:
                    ls = "--"
                plt.plot(
                    config.thresholdSetError,
                    attr.precisionList,
                    c=config.LINE_COLORS[i],
                    label="{0} [{1:.2f}]".format(tracker, attr.precisionList[20]),
                    lw=2.0,
                    ls=ls,
                )
            # else:
            #    plt.plot(config.thresholdSetError, attr.precisionList,
            #        label='', alpha=0.5, c='#202020', ls='--')
        else:
            print("err")
    plt.title("{0}_{1} (precision)".format(evalType, testname.upper()))
    plt.rcParams.update({"axes.titlesize": "medium"})
    plt.xlabel("Thresholds")
    plt.autoscale(enable=True, axis="x", tight=True)
    plt.autoscale(enable=True, axis="y", tight=True)
    plt.grid(color="#101010", alpha=0.5, ls=":")
    plt.legend(fontsize="medium")
    # plt.savefig(BENCHMARK_SRC + 'graph/{0}_sq.png'.format(evalType), dpi=74, bbox_inches='tight')
    plt.show()
    return plt


if __name__ == "__main__":
    main()
