# MSA Safety Hackathon

## Paper

Our final paper is [here](https://www.stevenshan.com/msa-safety-hackathon/docs/paper.pdf).

## Setup

Git LFS is required because some one of the zip files is 114 MB which is above the 100 MB limit Github imposes on file sizes. After installing Git LFS, run `git lfs pull` to download the zip files.

Run `python setup.py` to extract data files.

Run `python filter_csv.py` to produce the CSV files for Session Alarm files.

Run `python filt_period.py` to produce the CSV files for Periodic Data files.

These CSV files will contain the 'average', 'peak', and 'site' data fields from all files, which can be used to plot charts in Microsoft Excel. 
