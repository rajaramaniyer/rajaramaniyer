#!/opt/homebrew/opt/python@3.9/libexec/bin/python
import re

with open("/Users/rajaramaniyer/Movies/sanskrit.txt", 'r', encoding="UTF-8") as file:
    lines = file.readlines()

file=open("/Users/rajaramaniyer/Movies/sanskrit.txt", 'w', encoding="UTF-8")
i=1
for line in lines:
    if "*" in line:
        i=1
    if "॥" in line and "*" not in line:
        line=re.sub(r"\n", " " + str(i) + " ॥\n", line)
        i+=1
    file.write(line)
file.close()
