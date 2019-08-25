# Change Log
This document describes changes I've made to the Python code after forking from 
jwlim/tracker\_benchmark. All these changes were made so the tools will work
correctly on my workstation (Kubuntu and Python 3.6). Only minimal changes have
been made. For example, I only changed `import` statements if they caused a bug.
So some import statements that don't follow Python recommendations may have not
been changed.

## Importing Local Modules
I changed lines of the form `from foo import *`. This is considered a bad
practice, and it often failed on my workstation. I changed them proper forms
such as `import foo` or `from foo import bar`, etc.

This had ripple effects. In a few cases, I had to import a module which was no
longer implicitly imported.

I also had to use fully qualified names through out the code.

## Print Functions
I had to change Python 2 `print` statements to Python 3 `print()` functions. I
also changed formatted strings to Python 3 style.

## \_\_init.py\_\_ Files
Local modules have *\_\_init\_\_.py* files which just import everything locally.
These cause errors with Python 3, so I commented out the import statements.

## Remove Extra Graph Curves
In *draw_graph.py*, trackers with poor results were still drawn in the graph,
but with light gray color. Despite the light color, the graph was still
difficult to read. I commented out the code which draws the extra curves.

## Remove Use of maps
The original code uses `map` types quite often to delay generation of lists.
These would not work in my Python 3 environment. I replaced the `map`s with
generator expressions to create the lists immediately.

## Downloading Sequences
The code to download the video sequences did not work on my workstation. Rather
than work through the bugs, I disabled downloading in *config.py*, and
downloaded the sequences using my own script.

## Writing Files
The tools open text for writing in binary mode. Writing a string would then fail
because a string is not an array of bytes. I changed the `open()` function calls
so the files would open in text mode instead of binary.

## Running My Tracker
First, I copied the *run_MDNet.py* script, and modified it to run my modified
py-MDNet. My script is *run_dmdnet.py*.

Then, I had to modify the line in *run_trackers.py* which invokes my tracker's
run script. The original formatted string did not work correctly, so I hard
coded the string to invoke *run_dmdnet.py*.

## Missing precisionList Array
The function `scripts.butil.eval_results.calc_result()` was missing the
`precisionList` array variable. This resulted in a run time exception. I just
had initialization of an empty array.
