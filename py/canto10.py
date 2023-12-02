import json
import re

def get_lines(filename):
  file = open(filename, 'r', encoding="UTF-8")
  Lines = file.read().splitlines()
  file.close()
  return Lines

titles = [
    "The First Step in God Realization",
    "The Lord in the Heart",
    "Pure Devotional Service - The Change in Heart",
    "The Process of Creation",
    "The Cause of All Causes",
    "Purusha-sukta Confirmed",
    "Scheduled Incarnations with Specific Functions",
    "Questions by King Parikshit",
    "Answers by Citing the Lord's Version",
    "Bhagavatam Is the Answer to All Questions",
]

json_file = "C:/Users/rajar/Videos/automate-youtube/videosInPlayList-PLdBTiOEoG70nrGqDyA1AQvvZgRyPSmRoN.json"

f = open(json_file, "r", encoding="UTF-8")
playlist = json.load(f)
f.close()

i=0
for item in playlist:
    item['title'] = "Srimad Bhagavatham Canto 2 Chapter %02d | %s" % ((i+1), titles[i])
    print(item['title'] + str(len(item['title'])))
    i+=1

with open(json_file, "wt", encoding="UTF-8") as file:
    file.write(json.dumps(playlist, indent=2))
