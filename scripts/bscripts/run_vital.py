"""Run py-Vital."""

import json
import os.path
import subprocess
import sys

def run_vital(sequence, *unused):  # pylint: disable=unused-argument
    """Run the base py-Vital tracker.

    Parameters:
    sequence (string): The name of the sequence to run.
    rp: Unknown
    save_image (boolean): True indicates to save images with bounding boxes.
    False indicates to not.

    Returns:
    Tracking results as a JSON object.
    """

    vital_path = os.path.expanduser("~/repositories/py-Vital")
    sys.path.append(vital_path)
    tmp_res = os.path.join(vital_path, "tmp_res.json")
    seq_config = {}
    seq_config["seq_name"] = sequence.name
    seq_config["img_list"] = sequence.s_frames
    seq_config["init_bbox"] = sequence.init_rect
    seq_config["savefig_dir"] = ""
    seq_config["result_path"] = tmp_res

    tmp_config = os.path.join(vital_path, "tmp_config.json")
    tmp_config_file = open(tmp_config, "w")
    json.dump(seq_config, tmp_config_file, indent=2)
    tmp_config_file.close()

    curdir = os.path.abspath(os.getcwd())
    os.chdir(vital_path)
    command = map(str, ["python3", "tracking/run_tracker.py", "-j", tmp_config])
    subprocess.call(command)
    os.chdir(curdir)
    res = json.load(open(tmp_res, "r"))
    os.remove(tmp_res)
    os.remove(tmp_config)
    sys.path.remove(vital_path)
    return res
