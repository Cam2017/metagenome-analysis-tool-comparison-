# This script trims the paired-end-reads. It outputs trimmed single- and paired-end-reads and stores them in a created directory
# The input is a directory with FASTQ files 

# Required modules
from sys import argv
from shutil import rmtree
from os import mkdir, chdir, listdir, getcwd, system, path

def trim_paired_end_reads(fastq_files_dir = argv[1]):
	files = list()
	trimmed_dir = '../trimmed_dir/'

	# Go to the FASTQ files directory
	chdir(fastq_files_dir)

	# Remove an existing path
	if path.exists(trimmed_dir):
		rmtree(trimmed_dir)

	# Create a directory where the trimmed reads will be stored
	mkdir(trimmed_dir)

	# Collect and sort FASTQ files
	for elem in listdir(getcwd()):
		if not elem.startswith('.'): 
			files.append(elem)
	files.sort() # Change the order in the original list

	# Trim the paired-end-reads(quality=20, length=35) with the tool Sickle. Check Sickle for options
	for i in xrange(0,len(files),2):
		trim_forward_file = trimmed_dir + files[i]
		trim_reverse_file = trimmed_dir + files[i+1]
		trim_single_file = trimmed_dir + files[i].split('_')[0] + '_single.fastq'
		trim_arg = ('sickle pe -f', files[i], '-r', files[i+1], '-t sanger -o',\
			trim_forward_file, '-p', trim_reverse_file, '-s', trim_single_file, '-q 20 -l 35') 

		trim_cmd = ' '.join(trim_arg)
		system(trim_cmd) # Invoke the (system) command in a subshell

# Run the main program 
if __name__ == '__main__':
	trim_paired_end_reads()