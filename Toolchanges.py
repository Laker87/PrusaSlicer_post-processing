#!python

import sys
# import re

sourceFile=sys.argv[1]
# sourceFile="cube.gcode"

# Read the ENTIRE g-code file into memory
with open(sourceFile, "r") as file:
    lines = file.readlines()
    toolchanges = 0
    for index in range(len(lines)):
        line = lines[index]
        if line[:2] == 'T0' or line[:2] == 'T1':
            toolchanges += 1

with open(sourceFile, "w") as of:
    for index in range(len(lines)):
        line = lines[index]
        if line.startswith('START_PRINT'):
            line = line.replace('EXTRUDERS=0', 'EXTRUDERS=' + str(toolchanges))
            of.write(line)
        else:
            of.write(line)