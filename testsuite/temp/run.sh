#!/bin/bash
#
# This shell script runs the Python code (note it needs to be python3 to use the statistics package)
#
python3 ./src/find_political_donors.py ./input/itcont.txt ./output/medianvals_by_zip.txt ./output/medianvals_by_date.txt

