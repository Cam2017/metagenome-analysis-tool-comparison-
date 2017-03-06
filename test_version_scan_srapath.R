#!/usr/bin/env Rscript

# This script lists the full paths of the runs of the 30 selected samples and converts the runs from SRA into paired FASTQ files.
# The script uses as inputs first the SraRunInfo.csv file and then the 30_runs_file.txt file. The file 30_runs_file.txt contains one run per line. The FASTQ files contain the paired-end-reads
# The script outputs the file selected_30_samples.tsv which gives an overview of the runs

# How to get the SraRunInfo.csv file from https://www.ncbi.nlm.nih.gov/bioproject/271013:
# Click on "1572" (Number of Links for SRA Experiments) -> "Send to" -> Choose Destination "File" -> Choose Format "Runinfo" -> "Create File" 
# This SraRunInfo.csv file contains 1572 samples/runs (size of all runs: 638.93 GB and 1.20 T Bases) from which the script selects the 30 samples

arguments <- commandArgs(TRUE) # Command line arguments
sra_file = arguments[1]
runs_file = arguments[2]

# Read SRA file
SraRunInfo <- read.csv(sra_file)

# List the selected 30 samples/runs
selected_30_samples_list <-scan(runs_file, character(), quote="\"")

# Change the row names of SraRunInfo from numbers to runs
rownames(SraRunInfo) <- SraRunInfo[,1]

# Select the 30 samples/runs
selected_30_samples <- SraRunInfo[selected_30_samples_list,]

# Change row names of SraRunInfo back to numerical index
rownames(selected_30_samples)<-1:nrow(selected_30_samples)

# Write the dataframe "selected_30_samples" in the file "selected_30_samples.tsv"
write.table(selected_30_samples, file='selected_30_samples.tsv', quote=FALSE, sep='\t', col.names = NA)

# List the full paths of the 30 samples/runs files and convert their format from SRA into FASTQ. The FASTQ files contain the paired-end-reads
for (run in selected_30_samples_list) {
	run_full_path = paste("/scratch1/Allassane/my_pathomap/sratoolkit.2.8.1-ubuntu64/bin/srapath", run)
	convert_cmd = paste("/scratch1/Allassane/my_pathomap/sratoolkit.2.8.1-ubuntu64/bin/fastq-dump --split-3", run)

	# Invoke the (system) command
	system(run_full_path)
	system(convert_cmd)
}