#!/opt/homebrew/opt/python@3.9/libexec/bin/python

import json
import csv

with open('secondary-schools.json', "r") as file:
    schools=json.loads(file.read())

fields=[]
for school in schools:
    for key in school.keys():
        if key not in fields:
            fields.append(key)

table=[]
table.append(fields)
for school in schools:
    row=[]
    for field in fields:
        if field in school:
            if isinstance(school[field], list):
                row.append(','.join(school[field]))
            else:
                row.append(school[field])
        else:
            row.append('')
    table.append(row)

with open('secondary-schools.csv', "w") as f:
    write = csv.writer(f)
    write.writerows(table)
