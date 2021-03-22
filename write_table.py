"""Write tracking results to a LaTeX table."""

import argparse
import os
import statistics

import config
import scripts.butil.load_results
import scripts.butil.tables


def main():
    """The main entry point for the script."""
    arguments = _parse_command_line()
    trackers = _load_trackers(
        config.RESULT_SRC.format(arguments.evaluation_type), arguments.tracker
    )
    table = scripts.butil.tables.make_table(
        arguments.table_type, trackers, arguments.highlight_best, arguments.show_delta
    )
    score_list = _load_scores(trackers, arguments.evaluation_type, arguments.test_name)
    _extract_table(score_list, arguments.metric, table)
    print()
    table.print()


def _parse_command_line() -> argparse.Namespace:
    """
    Parse the command line arguments.

    :return: The parsed command line arguments.
    :rtype: argparse.Namespace
    """
    parser = argparse.ArgumentParser(
        description="Write overlap success or center error precision data to a LaTeX table.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "--evaluation-type",
        help="The type of evaluation to write.",
        choices=["OPE", "SRE", "TRE"],
        default="OPE",
    )
    parser.add_argument(
        "--highlight-best",
        help="For each category, highlight the best tracker score. The highlight is performed by "
        "a \\best{} LaTeX macro; you will need to define that macro in your LaTeX file.",
        action="store_true",
    )
    parser.add_argument(
        "--show-delta",
        help="Include a column showing the delta between the specified tracker and the best score.",
        metavar="TRACKER",
    )
    parser.add_argument(
        "--table-type",
        help="The type of table to print to the console.",
        choices=scripts.butil.tables.TABLE_TYPES,  # ["latex", "basic"],
        default="basic",
    )
    parser.add_argument(
        "test_name",
        help="The name of the test to write. This should match a name that you used when you ran "
        "the run_trackers.py script.",
    )
    parser.add_argument(
        "metric",
        choices=["overlap", "precision"],
        help="The type of graphs to draw: overlap success or center error precision.",
    )
    parser.add_argument(
        "tracker",
        help="The list of trackers to include in the table.",
        nargs="+",
    )
    return parser.parse_args()


def _load_trackers(results_directory: str, requested_trackers):
    """
    Load the list of the trackers available to graph.

    :param str results_directory: The directory that contains the tracking results. This directory
        is read to get the available trackers.
    :return: The list of available trackers.
    :rtype: list
    """
    possible_trackers = os.listdir(results_directory)
    trackers = []
    for tracker in requested_trackers:
        if tracker in possible_trackers:
            trackers.append(tracker)
        else:
            print("warning:", tracker, "is not available in", results_directory)
    return trackers


def _load_scores(trackers, evaluation_type, test_name):
    score_list = []
    for tracker in trackers:
        score_list.append(
            scripts.butil.load_results.load_scores(evaluation_type, tracker, test_name)
        )
    return score_list


def _extract_table(scores, metric: str, table: scripts.butil.tables.Table):
    """
    Extract the table data from the scores.

    :param list scores: The list of scores.
    :param str metric: The metric to report: overlap success or center error precision.
    :param scripts.butil.tables.Table table: The table to fill with score data.
    """
    if metric == "overlap":
        for tracker in scores:
            for category in tracker:
                table.set_value(
                    category.name,
                    category.tracker,
                    round(statistics.mean(category.successRateList), 2),
                )
    else:
        for tracker in scores:
            for category in tracker:
                table.set_value(
                    category.name,
                    category.tracker,
                    # TODO I copied this from draw_graph.py. Why is the median value used?
                    round(category.precisionList[20], 2),
                )


if __name__ == "__main__":
    main()
