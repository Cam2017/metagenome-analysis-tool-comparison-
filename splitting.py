# This script splits the MetaPhlAn2 and the MegaBLAST output files by ranks (family, genus and species)
# The input file is a text file in TSV format

# Required modules
from os import system
from os.path import basename, isfile
from sys import argv

def split_by_rank(ranks_info = ['f__', 'g__', 's__']):
	# The src_file must contain the word 'MetaPhlAn' or 'blast'
	# Warning: The src_file must not have a slash at the end
	src_file = argv[1] # Path of the source file

	# Check if the file path exists
	if isfile(src_file):
		pass
	else:
		print "The file path does not exist"
		exit(0)

	# Variables
	ranks = ranks_info
	filenames = [] # Empty list

	# Create file names and split the files by ranks (family, genus and species)
	for r in ranks:
		filename = r + basename(src_file)
		filenames.append(filename)

		if "MetaPhlAn" in src_file: # For MetaPhlAn2
			# Split the MetaPhlAn2 output file and add the two first lines of this file to the splitted file
			first_two_lines = "awk 'NR<=2 {print}'"
			extract_arg0 = (first_two_lines, src_file, '>', filenames[len(filenames)-1])
			extract_cmd0 = ' '.join(extract_arg0)
			system(extract_cmd0) # Execute the command in a subshell

		elif "blast" in src_file: # For MegaBLAST
			# Split the MegaBLAST output file and add the first line of this file to the splitted file
			first_line = "awk 'NR<=1 {print}'"
			extract_arg1 = (first_line, src_file, '>', filenames[len(filenames)-1])
			extract_cmd1 = ' '.join(extract_arg1)
			system(extract_cmd1) # Execute the command in a subshell

		else:
			print "The file is neither MetaPhlAn nor blast"

		# Parse by using awk and write the result in the splitted file
		extract_selected_ranks = "awk -F \"|\" '$NF ~ /^"+str(r)+"/ {print}'"
		extract_arg2 = (extract_selected_ranks, src_file, '>>', filenames[len(filenames)-1])
		extract_cmd2 = ' '.join(extract_arg2)
		system(extract_cmd2) # Execute the command in a subshell

	print filenames

# Run the main program
if __name__ == '__main__':
	split_by_rank()