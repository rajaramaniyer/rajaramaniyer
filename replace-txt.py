#!/usr/bin/env python3
from __future__ import print_function
import sys
import re

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

if len(sys.argv) != 2:
  filename = input ("Filename: ")
else:
  filename = sys.argv[1]

file = open(filename, 'r', encoding="UTF-8")
Lines = file.readlines()
file.close()

file = open(filename, "wt", encoding="UTF-8")
# Strips the newline character
for line in Lines:
    line=re.sub(r"\*+(\s+)?ebook converter DEMO Watermarks(\s+)?\*+(\n)?", "", line.replace("||", "॥").replace("।।", "॥").replace("|","।"))
    line=re.sub(r"।","।\n",line)
    line=re.sub(r"वाच ","वाच\n",line)
    line=re.sub(r"ऊचुः ","ऊचुः\n",line)
    line=re.sub(r"([१२३४५६७८९०]+(\s+)?(॥)?)",r"\1\n",line)
    while ( re.search("  ", line) ):
      line=re.sub("  "," ",line)
    file.write(line)
file.close()

file = open(filename, 'r', encoding="UTF-8")
Lines = file.readlines()
file.close()

file = open(filename, "wt", encoding="UTF-8")
# Strips the newline character
for line in Lines:
  line=re.sub(r" $","",line)
  line=re.sub(r"^ ","",line)
  if len(line)>1:
    line=re.sub(r"॥([^॥]+)\n$", r"॥\1॥\n\n",line)
    line=re.sub(r"॥ ", r"॥",line)
    file.write(line)
file.close()

# replace ॥ to ॥\n
# replace " \n" to \n
# replace "\n\n" to \n
# regex find ([१२३४५६७८९०]+(\s+)?(॥)?) and replace with $1\n
# regex find ॥(\s+)?([^॥]+)$ and replace with ॥$1॥
