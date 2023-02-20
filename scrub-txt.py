from __future__ import print_function
import sys
import re
import os.path
from os import path

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

if len(sys.argv) < 2:
  file_adyayam_number=""
  if path.exists("adyayam_number.txt"):
    f=open("adyayam_number.txt")
    file_adyayam_number = f.readlines()[0]
    f.close()
  adyayam_number = input ("Adhyayam Number(" + file_adyayam_number + "): ")
  if adyayam_number == "" and file_adyayam_number != "":
    adyayam_number = file_adyayam_number
else:
  adyayam_number = sys.argv[1]
f=open("adyayam_number.txt", "w")
f.write(adyayam_number)
f.close()

filename="C:/Users/rajar/srimad_bhaghavatham/sanskrit/canto01/chapter" + adyayam_number.zfill(2) + ".txt"
# filename="/Users/rajaramaniyer/Downloads/chapter" + adyayam_number.zfill(2) + ".txt"
file = open(filename, 'r', encoding="UTF-8")
data = file.read()
file.close()

data=re.sub(r"1","१", data)
data=re.sub(r"2","२", data)
data=re.sub(r"3","३", data)
data=re.sub(r"4","४", data)
data=re.sub(r"5","५", data)
data=re.sub(r"6","६", data)
data=re.sub(r"7","७", data)
data=re.sub(r"8","८", data)
data=re.sub(r"9","९", data)
data=re.sub(r"0","०", data)
data=re.sub(r"\|\|", "॥", data)
data=re.sub(r"\|", "।", data)
data=re.sub("।।", "॥", data)
data=re.sub("।।", "॥", data)
data=re.sub(r"\*+(\s+)?ebook converter DEMO Watermarks(\s+)?\*+", "", data)
data=re.sub(r"।(\s+)?", " ।\n", data)
data=re.sub(r"(॥)(\s+)?([१२३४५६७८९०]+)(\s+)?(॥)?(\s+)?", r"॥\3॥\n\n", data)
data=re.sub(r"॥ ","।\n", data)
data=re.sub("(\?|,|')", "", data)
while re.search(r"  ", data):
  data=re.sub("  ", " ", data)
data=re.sub(r"(ऊचुः|ध्यायः|वाच)", r"\1\n", data)
data=re.sub(r"-[१२३४५६७८९०]+(।|॥)\n", "", data)
data=re.sub(r"(.*)( लगे |यह | कहीं | कीजिये | रहे | हूँ | सारी | निकले | गयीं |उन्होंने |कीजिये |इसका |उन्हें |तुम | उनकी | तुमने | मेरे | करके | मैं | इन्हें | मैंने |उनका |उसकी | आये | हुए | लोगे | मालूम | लौट | हई |के पास | अपने | तरह | कई |हम | लोग | कोसके | कुचल | करें | डाला| गिर | अपनेसे )(.*)\n", "", data)
data=re.sub(r"(.*)( है | हैं | थे | की |होंगे | अब | थीं |जिस | में | दिया |और | थी | था | गये | करेंगे |उसके |उनके | हुआ | गयी | वह |लिये |साथ |सुनी | नहीं |होना |चाहिये |बाद |पहुँचे |आप |इस | गया | करेगा | किसी |उसने |उसे |उस |किया |पड़ेगा |तब )(.*)\n", "", data)
data=re.sub(r"(.*)( लगते | तुम्हारी | आपकी | आपका | मुझे | कुछ | अपनी | कर लो | करो | उतना | गिरते | सुनकर | हरा-भरा | ले लेते| लगाया | किसीका | इसी | बहुत | करती | इसमें | ओर | ही |कहा )(.*)\n", "", data)
while re.search(r" \n", data):
  data=re.sub(r" \n", r'\n', data)
while re.search(r"\n\n\n", data):
  data=re.sub(r"\n\n\n", r"\n\n", data)
data=re.sub(r"(इति श्रीमद्भागवते महापुराणे.*)\n(.*॥.*)\n", r"\1\2\n", data)
data=re.sub(r"(इति श्रीमद्भागवते महापुराणे.*)\n(.*\n)+", r"\1\n", data)

file = open(filename, "wt", encoding="UTF-8")
file.write(data)
file.close()
