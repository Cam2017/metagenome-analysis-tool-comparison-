# This script creates the workspace, collects and sorts the runs (in FASTQ format), generates the BAM files and executes the tool SLIMM

from preprocess import *

# Generate BAM files with the tool bowtie2 and put them in the BAM files directory
def generate_bam_files(bam_files_dir, files):
	bowtie2_software = '/scratch1/Temesgen/bin/bowtie2'
	bowtie2_db = '/scratch1/Temesgen/indices/bowtie2/AB_species/AB_species'

	for i in xrange(0,len(files),2):
		# Construct the path of the BAM file
		files_path_arg = (bam_files_dir, files[i].split('_')[0],'.bam')
		files_path = ''.join(files_path_arg)

		# Map the reads contained in the runs against the bowtie2 database and pipe the result directly into BAM format.
		# Check bowtie2 for options, e.g.: report up to 60 alignments per read (-k 60), threads 32 (-p 32)
		bowtie2_arguments = (bowtie2_software, '-x', bowtie2_db, '-1', files[i], '-2', files[i+1], '-q --no-unal --mm -p 32 -k 60 | samtools view -bS - >', files_path)
		bowtie2_cmd = ' '.join(bowtie2_arguments)
		system(bowtie2_cmd) # Execute the command in a subshell

# Generate the reports of all ranks (e.g. genus) with the tool SLIMM and put them in the created report directory. Check SLIMM for options
def get_slimm_report(bam_files_dir, report_dir, db = argv[1]):
	slimm_arg = ('slimm -m', db, '-d', bam_files_dir, '-o', report_dir, '-r all')
	slimm_cmd = ' '.join(slimm_arg)
	time_cmd = '\\time -v ' + slimm_cmd
	system(time_cmd) # Execute the command in a subshell

# Run the main program
if __name__ == "__main__":
	result_dir = '/scratch1/Allassane/my_pathomap/slimm_result/'
	report_dir = result_dir + 'slimm_report/'
	bam_files_dir = result_dir + 'aligned_bam_files/'
	files = prestep(result_dir, report_dir, bam_files_dir)
	generate_bam_files(bam_files_dir, files)
	get_slimm_report(bam_files_dir, report_dir)