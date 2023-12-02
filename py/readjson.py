import json
import re
import os

with open('C:/Users/rajar/Videos/automate-youtube/videosInPlayList-PLmozlYyYE-ERAkAKl-MbnQal-49xPVNwn.json', 'r') as file:
    jsonObjects = json.load(file)

f=1
for jsonObject in jsonObjects:
    file_name = 'C:/Users/rajar/books/narayaneeyam/narayaneeyam-' + str(f).zfill(3) + '.txt'
    if not os.path.exists(file_name):
        data = jsonObject['description'] + "\n"
        data = re.sub(r"\d+:\d+\s+", "", data)
        data = re.sub(r"All the verses.*\n", "", data)
        data = re.sub(r"(इति श्रीमन्नारायणीये.*)\n([^\n]*\n)+", r"\1\n", data)
        data = re.sub(r"\|\|", "॥", data)
        data = re.sub(r".*Shankararama.*\n", "", data)
        data = re.sub(r".*Visit.*\n", "", data)
        data = re.sub(r".*http.*\n", "", data)
        with open(file_name, 'w', encoding="UTF-8") as file:
            file.write(data)
    f+=1
