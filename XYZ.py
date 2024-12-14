#!python

# Cкрипт постобработки для прюши, который первое движение от места 
# парковки к точке начала печати совмещает в одно по всем осям. 
# По-умолчанию сделано, что сначала стол перемещается на высоту первого слоя, 
# а затем голова перемещается по XY осям в точку начала печати. 
# Данный скрипт меняет это поведение и движение происходит 
# сразу по 3 осям, голова едет в точку начала печати и 
# одновременно стол поднимается на высоту первого слоя.

import sys
import re
import os

sourceFile = sys.argv[1]

# Read the ENTIRE g-code file into memory
with open(sourceFile, "r") as f:
	lines = f.readlines()

if (sourceFile.endswith('.gcode')):
	destFile = re.sub('\.gcode$','',sourceFile)
	try:
		os.rename(sourceFile, destFile+".sqv.bak")
	except FileExistsError:
		os.remove(destFile+".sqv.bak")
		os.rename(sourceFile, destFile+".sqv.bak")
	destFile = re.sub('\.gcode$','',sourceFile)
	destFile = destFile + '.gcode'
else:
	destFile = sourceFile
	os.remove(sourceFile)

with open(destFile, "w", newline='\n') as of:
	# Find first Z move
	for index in range(len(lines)):
		line = lines[index]
		if line.startswith('G1 Z'):
			lineZ = line.lstrip("G1")
			firstZ = index
			break

	# Find first XY move
	for index in range(len(lines)):
		line = lines[index]
		if line.startswith('G1 X') or line.startswith('G1 Y'):
		# lineZ = line.lstrip("G1")
			firstXY = index
			break

	for index in range(len(lines)):
		line = lines[index]
		if index == firstZ:
			line = line.replace(line, '')
		if index == firstXY:
			line = line.replace(line, line.strip() + lineZ)
		of.write(line)

of.close()
f.close()