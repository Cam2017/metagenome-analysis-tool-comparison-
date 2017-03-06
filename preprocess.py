#!/usr/bin/env python

# This script is used by GOTTCHA, Kraken and SLIMM
# It is the basis for the creation of the workspace and the collection and sorting of the runs in FASTQ files

# Required modules
from shutil import rmtree
from os import mkdir, chdir, listdir, getcwd, system, path
from sys import argv

# Create the workspace
def create_workspace(list_direc):
	# Remove an existing path
	if path.exists(list_direc[0]):
		rmtree(list_direc[0])

	# Create directories
	for d in list_direc:
		mkdir(d)

# Collecting and sorting FASTQ files
def collect_sort_files(files):
	for elem in listdir(getcwd()):
		if not elem.startswith('.'): 
			files.append(elem)

	files.sort() # Change the order in the original list
	return files

def prestep(result_dir, report_dir, bam_files_dir = '', fastq_files_dir = argv[2], files=[]):
	if bam_files_dir:
		bam_files_dir = result_dir + 'aligned_bam_files/'
		list_direc = [result_dir, report_dir, bam_files_dir]
	else:
		list_direc = [result_dir, report_dir]

	# Execute the functions
	create_workspace(list_direc)
	chdir(fastq_files_dir) # Go into the directory which contains the FASTQ files
	collect_sort_files(files)

	return files