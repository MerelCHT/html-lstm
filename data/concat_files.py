"""
@author: Tobias Rijken
"""

import sys

def main(args):
	result = ""

	# Open all files and concat
	for i in range(1,len(args)):
		with open(args[i], 'r') as f:
			text = f.read()
		result += text

	# Write new string to file
	with open("complete_files.txt", "w") as f:
		f.write(result)

	return 0

if __name__ == '__main__':
	main(sys.argv)