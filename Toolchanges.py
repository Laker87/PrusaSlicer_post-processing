#!python

# -------------------------------------- #
# Скрипт пост обработки G-code файла для PrusaSlicer и SuperSlicer
# Анализирует файл и подсчитывает количество используемых для печати модели печатающих голов. 
# Модифицирует параметр EXTRUDERS макроса START_PRINT, добавляя туда полученное значение смен инструмента.
# На основании этого значения макрос START_PRINT при старте печати будет нагревать первый, второй или оба хотенда, 
# в зависимости от используемых для печати конкретной модели.
# Использование: добавить в скрипты постобработки слайсера скрипт: "C:\Program Files\Python310\python.exe" "D:\Soft\SuperSlicer\Toolchanges.py";
# Перый путь - это путь к исполняемому файлу python, второй - путь к скрипту.
# В макросе START_PRINT в слайсере значение EXTRUDERS установить 0: 
# START_PRINT EXTRUDER=[current_extruder] EXTRUDERS=0 EXTRUDER_TEMP={first_layer_temperature[0]} EXTRUDER1_TEMP={first_layer_temperature[1]} BED_TEMP={first_layer_bed_temperature}

import sys
# import re

sourceFile=sys.argv[1]

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
