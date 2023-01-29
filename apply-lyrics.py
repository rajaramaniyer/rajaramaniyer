#!/opt/homebrew/opt/python@3.9/libexec/bin/python

from operator import inv
from os import path
import re
import sys

def get_lines(filename):
  file = open(filename, 'r', encoding="UTF-8")
  Lines = file.read().splitlines()
  file.close()
  return Lines

sanskrit=[]
tamil=[]
if path.exists('sanskrit.txt'):
    file=open('sanskrit.txt', encoding='utf-8')
    sanskrit=file.read().splitlines()
    file.close()

if path.exists('tamil.txt'):
    file=open('tamil.txt', encoding='utf-8')
    tamil=file.read().splitlines()
    file.close()

#
# Main Code Starts
#
if len(sys.argv) != 2:
  olive_file_name=input("OveFileName: ")
else:
  olive_file_name=sys.argv[1]

Lines=get_lines(olive_file_name)

sitem=0
titem=0
file=open(olive_file_name.replace('.ove', '-new.ove'), 'w', encoding='utf-8')
for line in Lines:
    newline=line
    if "Sanskrit Text" in line:
        while sitem<len(sanskrit) and (len(sanskrit[sitem]) < 1):
            sitem += 1
        if sitem<len(sanskrit):
            newline=line.replace('Sanskrit Text', sanskrit[sitem])
        sitem+=1

    if "Tamil Text" in line and titem<len(tamil):
        while titem<len(tamil) and (len(tamil[titem]) < 1):
            titem += 1
        if titem<len(tamil):
            newline=line.replace('Tamil Text', tamil[titem])
        titem+=1
    file.write(newline)
    file.write('\n')
file.close()
