# This script creates the workspace, collects and sorts the runs (in FASTQ format), and executes the tool GOTTCHA

from preprocess import *

# Generate the reports of all ranks (e.g. genus) with the tool GOTTCHA and put them in the created report directory
def get_gottcha_report(files, report_dir, db = argv[1]):
	software_location = '/scratch1/Allassane/my_pathomap/gottcha/bin/gottcha.pl'

	for i in xrange(0,len(files),2):
		# Multiple files should be separated with a comma. Otherwise GOTTCHA cannot be executed
		combine_files = (files[i], ',', files[i+1]) 
		paired_end_files = ''.join(combine_files)

		# The option --threads 32 is used for GOTTCHA, as SLIMM uses all available cores for some part of the computation. Check GOTTCHA for options
		gottcha_arguments = (software_location, '--threads 32 --mode summary --input', paired_end_files, '--database', db, '-o', report_dir, '-p', files[i].split('_')[0])
		gottcha_cmd = ' '.join(gottcha_arguments)
		system(gottcha_cmd) # Execute the command in a subshell

# Run the main program
if __name__ == "__main__":
	result_dir = '/scratch1/Allassane/my_pathomap/gottcha_result/'
	report_dir = result_dir + 'gottcha_report/'
	files = prestep(result_dir, report_dir)
	get_gottcha_report(files, report_dir)