#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug  3 21:15:09 2023

@author: kelseyrichardson

Use: automate mean and standard deviation calcs for multiple contact angle measurements
"""

import numpy as np
import pandas as pd

# INPUTS:
    # user inputs:
        # - sample names
        # - number of slides per sample
        # - number of runs per slide
    # data inputs:
        # - .LOG file of contact angle measurements w/ following headings
        # No.  Time Theta(L) Theta(R)  Mean    Dev.  Height  Width   Area   Volume  Messages
# OUTPUTS:
    # - .xlsx file with sample name, slide #, run #, mean, and standard deviation

# format of data:
    # different directory for each sample (ex: A, B, etc.)
    # within sample directory, there are different directories for each run (ex: 'A slide 1 run 1', 'A slide 1 run 2', 'A slide 2 run 1')
    # within each run directory, there is a .LOG file for each contact angle measurement

# get user input about sample, run, and slide info
samples = input("Enter sample names, separated by a space: ")
samples = samples.split(" ")
slides = int(input("Enter number of slides per sample: "))
runs = int(input("Enter number of runs per slide: "))


# - - - - - FUNCTION TO CACULATE MEAN AND STD FOR SINGLE RUN - - - - - - - - -
def analyze_run(infile):
    
    # read through the lines in the file
    with open(infile) as f:
        f = f.readlines()
        
    # create empty array to hold measurement mean values
    meas_mean = []
    
    for line in f:
        # check if the line is the header
        if "No." in line:
            header = line
        else:
            # if not the header, pull out the mean value and store in array
            data = np.array(line.split(), dtype=float)
            meas_mean = np.append(meas_mean, data[4])
    
    # calculate mean and standard deviation of mean values
    run_mean= np.mean(meas_mean)
    run_std = np.std(meas_mean)
    return(run_mean,run_std)
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

# create empty arrays for lists that will become the data frame
sample_list = []
slide_list = []
run_list = []
mean_list = []
stdev_list = []

# loop through each sample, slide, and run
for sample in samples:
    # this sample_directory is defined as if the code is in the parent folder for samples
    # ** CHANGE BASED ON WHERE THE CODE AND MEASUREMENT DATA IS STORED **
    sample_directory = sample
    for slide in range(slides):
        # add one to convert from python indexing to actual numbering
        slide_str = slide + 1
        for run in range(runs):
            # add one to convert from python indexing to actual numbering
            run_str = run + 1
            # create path to files
            run_directory = sample_directory + '/' + sample + ' slide ' + str(slide_str) + ' run ' + str(run_str) + '/'
            infile = run_directory + 'CA_Buffer_' + sample + '_Slide' + str(slide_str) + '_Run' + str(run_str) + '.LOG'
            # calculate mean and standard deviation of each run
            mean, dev = analyze_run(infile)
            # add values to lists
            sample_list.append(sample)
            slide_list.append(slide+1)
            run_list.append(run+1)
            mean_list.append(mean)
            stdev_list.append(dev)

# create data frame from lists and output to excel
contact_data = pd.DataFrame({'Sample': sample_list, 'Slide': slide_list, 'Run': run_list, 'Mean': mean_list, 'Standard Deviation': stdev_list})
contact_data.to_excel("buffer_stats.xlsx")