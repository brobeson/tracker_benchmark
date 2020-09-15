"""Draw results graphs."""

import os
import sys
import matplotlib.pyplot as plt
import config
from scripts.butil import load_results, graphs


def main():
    """The main entry point for the script."""
    evalTypes = ["OPE"]
    testname = "tb100"
    graph = "overlap"
    if len(sys.argv) >= 2:
        graph = sys.argv[1]

    for i, evalType in enumerate(evalTypes):
        result_src = config.RESULT_SRC.format(evalType)
        trackers = os.listdir(result_src)
        tracker_colors = graphs.get_color_table(trackers)
        scoreList = []
        for t in trackers:
            score = load_results.load_scores(evalType, t, testname)
            scoreList.append(score)
        if graph == "precision":
            graph = get_precision_graph(scoreList, i, evalType, testname)
        else:
            graph = get_overlap_graph(scoreList, i, evalType, testname, tracker_colors)
    graph.show()


def get_overlap_graph(scoreList, figure_number, evalType, testname, tracker_colors):
    """Generate the overlap success graph."""
    graphs.draw_overlap(scoreList, tracker_colors, "dmdnet")
    sys.exit(0)
    plt.figure(num=figure_number, figsize=(9, 6), dpi=70)
    rankList = sorted(scoreList, key=lambda o: sum(o[0].successRateList), reverse=True)
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


def get_precision_graph(scoreList, figure_number, evalType, testname):
    """Generate a center precision error graph."""
    plt.figure(num=figure_number, figsize=(9, 6), dpi=70)
    rankList = sorted(scoreList, key=lambda o: o[0].precisionList[20], reverse=True)
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
