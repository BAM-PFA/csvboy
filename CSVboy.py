#!/usr/bin/env python3
import argparse
# import chardet
import csv
import os
import string
from unidecode import unidecode
'''
This script will take in a CSV ("--dataPath=/path/to/data.csv") and look for 
any characters that could cause problems. In all cases, any UTF-8 BOM that 
exists will be removed. You can also specify whether you want to 
'transliterate' characters to their closest UTF-8 analogues (mode='ascii'),
whether you want to leave valid UTF-8 characters as-is (mode='utf-8'), or 
whether you want to replace them with a character of your choosing 
(mode='replace'; the default is "_").

The resulting data will be written out to a new CSV. You can specify
a location for the new CSV ("--outPath=/your/path")or just let the script put 
it in the same folder as the input CSV.
'''

def strip_BOM(firstLast):
	'''
	Take in the first and last lines of the CSV.
	Look at the first character if the first element in the first line
	and the last character of the last line and look for a BOM. 
	Remove it if necessary.
	'''
	stripped = []
	for idx in (0,-1):
		try:
			firstLast[idx][idx] = [
				x.replace('\ufeff','') for x in firstLast[idx] 
					if '\ufeff' in x
						][0]
		except:
			firstLast[idx][idx] = firstLast[idx][idx]
	
	return firstLast

def get_output_path(dataPath):
	outPath = os.path.dirname(dataPath)
	print(outPath)
	if os.path.isdir(outPath):
		pass
	else:
		# just put it on the desktop
		print("something fishy happend, we'll output to your Desktop")
		outPath = os.path.expanduser("~/Desktop")

	return outPath

def sanitize(dataPath,
	replacementCharacter,
	outPath,
	mode):
	'''
	Go through the CSV looking for characters that could cause problems.
	Depending on the user-defined `mode`, replace characters or don't.
	'''
	# if the user didn't specify an output path,
	# default to the same directory as the input
	if not outPath:
		outPath = get_output_path(dataPath)

	print(replacementCharacter)

	basename = os.path.basename(dataPath)
	splitname = os.path.splitext(basename)
	# the output file gets _sanitized appended
	sanitizedBasename = splitname[0]+"_sanitized"+splitname[1]
	outCSVpath = os.path.join(outPath,sanitizedBasename)

	with open(dataPath,'r') as f:
		reader = csv.reader(f)

		lines = [] # we'll iterate over each line in the CSV as a list
		outputLines = [] # this will be a list of lines for the new CSV
		
		for line in reader:
			lines.append(line)

		# STRIP OUT ANY BOM IF IT EXISTS
		firstLast = [lines[0],lines[-1]]
		firstLast = strip_BOM(firstLast)
		lines[0] = firstLast[0]
		lines[-1] = firstLast[-1]

		# GO THROUGH EACH LINE AND LOOK AT EACH CARACTER IN EACH ITEM
		for line in lines:
			lineIndex = lines.index(line) # we'll use this to replace values
			# `item` is a cell value in the CSV
			for item in line:
				# build a list of the indexes of any characters 
				# that are not pure ASCII
				questionable = [
					item.index(char) for char in item 
						if char not in string.printable
					]
				if questionable:
					# if there's any non-ASCII-type characters, look closer
					# based on the user defined mode
					if mode == 'ascii':
						for idx in questionable:
							lines[lineIndex] = [
								item.replace(
									item[idx],unidecode(item[idx])
									) for item in lines[lineIndex]
								]
					elif mode == 'replace':
						for idx in questionable:
							lines[lineIndex] = [
								item.replace(item[idx],replacementCharacter)
									for item in lines[lineIndex]
								]
					elif mode == 'utf-8':
						for idx in questionable:
							try:
								item[idx].encode('utf-8')
							except UnicodeDecodeError:
								# if it's not valid unicode, 
								# just remove the character?
								# otherwise I could 
								lines[lineIndex] = [
									item.replace(item[idx],"")
										for item in lines[lineIndex]
									]


			outputLines.append(lines[lineIndex]) # add the line to the output list

	with open(outCSVpath,'w') as f:
		writer = csv.writer(f)
		for line in outputLines:
			writer.writerow(line)

	return outCSVpath

def set_args():
	parser = argparse.ArgumentParser()
	parser.add_argument(
		'-d','--dataPath',
		help='path to data CSV file',
		required=True
		)
	parser.add_argument(
		'-r','--replacementCharacter',
		help='character to replace illegal characters with',
		default="_"
		)
	parser.add_argument(
		'-o','--outPath',
		help='output csv directory path (default is same as input)'
		)
	parser.add_argument(
		'-m','--mode',
		help=(
			"Choose from:\n"
			"ascii (strip BOM, translate all characters to ascii-compliant utf-8)\n"
			"utf8 (only strip BOM, keep valid utf8 chars as-is but"
				" transliterate invalid chars to ascii)\n"
			"replace (strip BOM, replace any weird characters with "
				"desired replacementCharacter"
			),
		choices=['ascii','utf8','replace'],
		default='utf8'
		)

	return parser.parse_args()

def main():
	args = set_args()

	dataPath = args.dataPath
	replacementCharacter = args.replacementCharacter
	outPath = args.outPath
	mode = args.mode
	print(outPath)

	options = {
	'replacementCharacter':replacementCharacter,
	'outPath':outPath,
	'mode':mode
	}

	newCsv = sanitize(dataPath,**options)

	print("check out the sanitized file at "+newCsv)

if __name__ == '__main__':
	main()
