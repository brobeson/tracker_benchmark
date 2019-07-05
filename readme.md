Tracker Benchmark (Tested on python 2.7.10)

Usage
- Default (for all trackers, all sequences, all evaluation types(OPE, SRE, TRE))
  - command: `python run_trackers.py`

- For specific trackers, sequences, evaluation types
  - command:
    `python run_trackers.py -t "tracker" -s "sequence" -e "evaluation type"`
  - sequence can be name of Sequence, 'tb50', 'tb100' and 'cvpr13' (using
    data/tb\_50.txt, tb\_100.txt, cvpr13.txt)
  - e.g.
    - `python run_trackers.py -t IVT,TLD -s Couple,Crossing -e OPE,SRE`
    - `python run_trackers.py -s tb50`

- Plotting
  - Success rate plotting command: `python draw_graph.py`
  - Precision plotting command: `python draw_graph.py precision`
  - Draw bounding box results: `python draw_bbox.py`

Libraries
- Matlab Engine for python (only needed for executing Matlab script files of
  trackers) http://kr.mathworks.com/help/matlab/matlab-engine-for-python.html
- matplotlib
- numpy
- Python Imaging Library (PIL) http://www.pythonware.com/products/pil/

Troubleshooting
- Segmentation Fault when running `python run_tracker.py ...` on MacOSX
  - Set DYLD\_LIBRARY\_PATH environment variable.
  - e.g.: export DYLD\_LIBRARY\_PATH=/usr/local/Cellar/python/2.7.11/Frameworks/Python.framework/Versions/Current/lib/:$DYLD\_LIBRARY\_PATH
