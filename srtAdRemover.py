##
## SRT SUBTITLE AD REMOVER
##
## This small python script allows you to remove ads from subtitles. This script will go over each line 
## in the SRT file and will check against a list of predefined ad identifiers. If a line contains any 
## of those ad identifiers, the full subtitle block (meaning all the data needed to display the subtitle, 
## including the timestamps) will be removed from the file. 
##
## If an ad isn't being recognized by the script, you can simply add the identifier to the list 
## of predefined ad identifiers and it will be deleted when you run the script.
##
## USAGE
## 
## SINGLE FILE: python srtAdRemover.py "[[PATH-TO-SRT-SUBTITLE-FILE]]"
## 		Example: python srtAdRemover.py "/Series/How I Met Your Mother/Season 5/How I Met Your Mother - S05E02.en.srt"
## BULK: python srtAdRemover.py bulk "[[PATH-TO-FOLDER]]"
##		Example: python srtAdRemover.py "/Series/How I Met Your Mother/Season 5"
##				 python srtAdRemover.py "/Series/How I Met Your Mother"
##
## BAZARR
##
## You can use this script together with Bazarr:
## - In your Bazarr instance, navigate to 'Settings' > 'Subtitles'
## - Check 'Use Custom Post-Processing'
## - Add the following command to 'Post-processing command': python [[PATH-TO-THIS-SCRIPT]]/srt-ad-remover.py "{{subtitles}}"
##
## 
## Created by Michaël Soetaert
##
## Version: 1.0.0

import requests # Install with 'pip3 install requests'.
import sys
import glob
import os

# Array of ad identifiers.
adIdentifiers = [
	'NapiProjekt',
	'HumanGuardians',
	'OpenSubtitles',
	'Formule1',
	'Advertise your product',
	'Flixtor',
	'WWW.NL',
	'AmericasCardroom',
	'DePrivacyShop',
]


def main(arguments):
	# python 'python-file-name' 'argument-1'
	if (len(arguments) == 2):
		# Remove ads from a single file.
		if arguments[1].endswith('.srt'):
			removeAds(arguments[1])
		else:
			print('Argument doesn\'t point to a SRT file. (If 1 argument is provided, it is expected to point to a SRT file)')
	# python 'python-file-name' 'argument-1' 'argument-2'
	elif (len(arguments) == 3):
		# Bulk remove ads from files.
		if arguments[1] == 'bulk':
			bulkRemoveAds(arguments[2])
		else:
			print('Argument 1 should be \'bulk\'. (If 2 arguments are provided, it is expected to be a \'bulk\'-command)')
	else:
		# python 'python-file-name'
		if (len(arguments) == 1):
			print('Arguments are required to use this script. (Please see the README.md file for an explanation)')
		# python 'python-file-name' 'argument-1' 'argument-2' 'argument-3' ...
		if (len(arguments) > 3):
			print ('I\'ve got no idea what to do with all those arguments. (This scripts accepts a maximum of 2 arguments)')

# Processes all SRT files in a provided root path.
def bulkRemoveAds(rootFolder):
	# Retrieve all the relative paths of the SRT files.
	srtFiles = glob.glob(rootFolder + '/**/*.srt', recursive=True)
	# Count the SRT files.
	amountOfSrtFiles = len(srtFiles)
	# Loop all the SRT files.
	for index, srtFile in enumerate(srtFiles):
		# Get the absolute path.
		absolutePath = os.path.abspath(srtFile)
		# Provide that path to the 'removeAds'-function to process the file.
		removeAds(absolutePath)
		# Provide feedback.
		print('(' + str(index + 1) + '/' + str(amountOfSrtFiles) + ') - Processed "' + absolutePath + '".')

# Remove ads from an SRT file with the provided file path.
def removeAds(filePath):

	# Open the 'SRT'-file.
	srtFile = openFile(filePath)
	# Read the lines of the 'SRT'-file.
	srtFileLines = srtFile.readlines()

	# Empty dictionary that will contain all the ad blocks in the SRT file.
	adBlocks = {}

	# Loop the lines and search for any ads in the SRT file.
	for index, line in enumerate(srtFileLines):
		# Decode the line to avoid any errors.
		line = line.decode(errors='replace')
		# Check if the current line contains any ads.
		if isAd(line):
			adIndex = index
			adBlockStart = None 
			adBlockEnd = None
			# Loop back until we find the timestamp line for the ad.
			while True:
				if isTimeStamp(srtFileLines[adIndex].decode(errors='replace')):
					adBlockStart = adIndex - 1
					break;
				adIndex -= 1
			# Loop further until we find the next timestamp line, so that we know where our subtitle block stops.
			adIndex = index
			while True:
				if adIndex == len(srtFileLines):
					adBlockEnd = adIndex
					break;
				if isTimeStamp(srtFileLines[adIndex].decode(errors='replace')):
					adBlockEnd = adIndex - 2
					break;
				adIndex += 1
			# Add the start and end to the array.
			adBlocks[adBlockStart] = adBlockEnd

	# Point back to the first line.
	srtFile.seek(0)

	# Get all line numbers from the ad blocks.
	lineNumbers = getLineNumbers(adBlocks)
	
	# Boolean that will indicate if new data has been written to the file.
	newDataWritten = False

	# Loop the file again and remove the lines.
	for index, line in enumerate(srtFileLines):
		if index not in lineNumbers:
			srtFile.write(line)
			newDataWritten = True

	# If new data has been written to the file, remove everything after the last write.
	if newDataWritten:
		srtFile.truncate()

	# Close the file.
	srtFile.close()

# Open the file with the provided path.
def openFile(filePath):
	return open(filePath, 'rb+')

# Checks if the provided line contains an ad.
def isAd(fileLine):
	# Loop array with all ads and check if any is present in our file.
	for adIdentifier in adIdentifiers:
		if adIdentifier in fileLine:
			return True

	return False

# Checks if the provided line is a timestamp line.
def isTimeStamp(fileLine):
	return True if '-->' in fileLine else False

# Retrieves the line numbers for the provided blocks.
def getLineNumbers(blocks):
	lineNumbers = []

	for index in blocks:
		i = index
		while i <= blocks[index]:
			lineNumbers.append(i)
			i += 1

	return lineNumbers

if __name__ == '__main__':
	main(sys.argv)

