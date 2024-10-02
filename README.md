# Post-processing in Python for Nek5000.
Used to post-process data from a Nek5000 simulation.  The `run` folder contains a number of files containing functions used to post-process Nek files, while the parent directory contains `postprocess.py` which is used to set of processing runs.  It is a little convoluted and not very well written so feel free to reach out if it is confusing. The `shell_scripts` folder contains some scripts I used when processing Nek5000 simulations, they may be useful to someone.

In `run/tools` are the basic Python functions that read the Nek5000 data from the simulation0.f00001 files.  Some functions may only be relevant to the cases I was looking at at the time.

The functions `readnek` and `reshapenek` in `run/tools/readingNek.py` are the ones that read and reshape the `*0.f00001` files and will likely be the most useful.
