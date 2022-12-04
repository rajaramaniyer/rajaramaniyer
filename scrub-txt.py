from __future__ import print_function
import sys
import re
import os.path
from os import path

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

if len(sys.argv) != 2:
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

filename="C:/Users/rajar/srimad_bhaghavatham/sanskrit/canto10/chapter" + adyayam_number + ".txt"
file = open(filename, 'r', encoding="UTF-8")
data = file.read()
file.close()

file = open(filename, "wt", encoding="UTF-8")
data=re.sub(r"-[१२३४५६७८९०]+(।|॥)\n", "",
    re.sub(r"(.*)( लगे |यह | कहीं | कीजिये | रहे | हूँ | सारी | निकले | गयीं |उन्होंने |कीजिये |इसका |उन्हें |तुम | उनकी | तुमने | मेरे | करके | मैं | इन्हें | मैंने |उनका |उसकी | आये | हुए | लोगे | मालूम | लौट | हई |के पास | अपने | तरह | कई |हम | लोग | कोसके | कुचल | करें | डाला| गिर | अपनेसे )(.*)\n", "",
      re.sub(r"(.*)( है | हैं | थे | की |होंगे | अब | थीं |जिस | में | दिया |और | थी | था | गये | करेंगे |उसके |उनके | हुआ | गयी | वह |लिये |साथ |सुनी | नहीं |होना |चाहिये |बाद |पहुँचे |आप |इस | गया | करेगा | किसी |उसने |उसे |उस |किया |पड़ेगा |तब )(.*)\n", "",
        re.sub(r"(ऊचुः|ध्यायः|वाच) ", r"\1\n\n",
          re.sub("  ", " ",
            re.sub("(\?|,|')", "",
              re.sub(r"॥ ","।\n",
                re.sub(r"(॥)(\s+)?([१२३४५६७८९०]+)(\s+)?(॥)?(\s+)?", r"॥\3॥\n\n",
                  re.sub(r"।(\s+)?", " ।\n", 
                    re.sub(r"\*+(\s+)?ebook converter DEMO Watermarks(\s+)?\*+", "",
                      re.sub("।।", "॥", 
                        re.sub(r"\|", "।", 
                          re.sub(r"\|\|", "॥", data)
                        )
                      )
                    )
                  )
                )
              )
            )
          )
        )
      )
    )
  )
data=re.sub(r"(.*)( लगते | तुम्हारी | आपकी | आपका | अपनी | कर लो | करो | उतना | गिरते | सुनकर | हरा-भरा | ले लेते| लगाया | किसीका | इसी | बहुत | करती | इसमें | ओर )(.*)\n", "",
  data
)
file.write(data)
file.close()

#file = open(filename, 'r', encoding="UTF-8")
#Lines = file.readlines()
#file.close()
#
## Strips the newline character
#file = open(filename, "wt", encoding="UTF-8")
#prev_line=""
#for line in Lines:
#  if (line == "\n" and prev_line != "\n") or "इति" in line:
#    file.write(line)
#  prev_line = line
#file.close()

file = open(filename, 'r', encoding="UTF-8")
data = file.read()
file.close()

file = open(filename, "wt", encoding="UTF-8")
while re.search(r"\n\n\n", data):
  data = re.sub(r"\n\n\n", "\n\n", data)
file.write(data)
file.close()
