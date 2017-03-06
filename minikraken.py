# This script creates the workspace, collects and sorts the runs (in FASTQ format), and executes the tool Kraken (MiniKraken)

from preprocess import *

# Generate the reports of all ranks (e.g. genus) with the tool Kraken and put them in the created report directory
def get_kraken_report(files, report_dir, db = argv[1]):
	software_report = 'kraken-report --db'

	for i in xrange(0,len(files),2):
		# Construct the path of the Kraken report file
		files_path_arg = (report_dir, files[i].split('_')[0], '_kraken_report.tsv')
		files_path = ''.join(files_path_arg)

		# The option --threads 32 is used for Kraken, as SLIMM uses all available cores for some part of the computation. Check Kraken for options
		kraken_arguments = ('kraken --threads 32 --paired --db', db, '--fastq-input', files[i], files[i+1], '|', software_report, db, '>', files_path)
		kraken_cmd = ' '.join(kraken_arguments)
		system(kraken_cmd) # Execute the command in a subshell

# Run the main program
if __name__ == "__main__":
	result_dir = '/scratch1/Allassane/my_pathomap/kraken_result/'
	report_dir = result_dir + 'kraken_report/'
	files = prestep(result_dir, report_dir)
	get_kraken_report(files, report_dir)