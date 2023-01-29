#!/opt/homebrew/bin/python3
from operator import inv
import re

sfile=open('sanskrit.txt', encoding='utf-8')
slines=sfile.read().splitlines()
sfile.close()

tfile=open('tamil.txt', encoding='utf-8')
tlines=tfile.read().splitlines()
tfile.close()

ofile=open('SriNathaAshtakam.ove', encoding='utf-8')
olines=ofile.read().splitlines()
ofile.close()

file=open('SriNathaAshtakamFinal.ove', 'w', encoding='utf-8')
for line in olines:
    if "Title" in line:
        rr=re.search(r"in=\"(\d+)\" out=\"(\d+)\"",line)
        inValue = int(rr.group(1))
        outValue = int(rr.group(2))
        diffValue = outValue - inValue - 1
    if "<field id=\"posx\" value=\"945\"/>" in line:
        file.write('                        <field id="posx" value="2880">\n')
        file.write('                            <key value="-965" frame="0" type="0" prehx="-40" prehy="0" posthx="40" posthy="0"/>\n')
        file.write('                            <key value="945" frame="20" type="0" prehx="-40" prehy="0" posthx="40" posthy="0"/>\n')
        file.write('                            <key value="2880" frame="' +str(diffValue)+ '" type="0" prehx="-40" prehy="0" posthx="40" posthy="0"/>\n')
        file.write('                            <key value="945" frame="' +str(diffValue-20)+ '" type="0" prehx="-40" prehy="0" posthx="40" posthy="0"/>\n')
        file.write('                        </field>\n')
    elif "<field id=\"posy\" value=\"515\"/>" in line:
        file.write('                        <field id="posy" value="515">\n')
        file.write('                            <key value="515" frame="0" type="0" prehx="-40" prehy="0" posthx="40" posthy="0"/>\n')
        file.write('                            <key value="515" frame="20" type="0" prehx="-40" prehy="0" posthx="40" posthy="0"/>\n')
        file.write('                            <key value="515" frame="' +str(diffValue)+ '" type="0" prehx="-40" prehy="0" posthx="40" posthy="0"/>\n')
        file.write('                            <key value="515" frame="' +str(diffValue-20)+ '" type="0" prehx="-40" prehy="0" posthx="40" posthy="0"/>\n')
        file.write('                        </field>\n')
    elif "<field id=\"posx\" value=\"975\"/>" in line:
        file.write('                        <field id="posx" value="-965">\n')
        file.write('                            <key value="2880" frame="0" type="0" prehx="-40" prehy="0" posthx="40" posthy="0"/>\n')
        file.write('                            <key value="975" frame="20" type="0" prehx="-40" prehy="0" posthx="40" posthy="0"/>\n')
        file.write('                            <key value="975" frame="' +str(diffValue-20)+ '" type="0" prehx="-40" prehy="0" posthx="40" posthy="0"/>\n')
        file.write('                            <key value="-965" frame="' +str(diffValue)+ '" type="0" prehx="-40" prehy="0" posthx="40" posthy="0"/>\n')
        file.write('                        </field>\n')
    elif "<field id=\"posy\" value=\"549\"/>" in line:
        file.write('                        <field id="posy" value="549">')
        file.write('                            <key value="549" frame="0" type="0" prehx="-40" prehy="0" posthx="40" posthy="0"/>')
        file.write('                            <key value="549" frame="20" type="0" prehx="-40" prehy="0" posthx="40" posthy="0"/>')
        file.write('                            <key value="549" frame="' +str(diffValue-20)+ '" type="0" prehx="-40" prehy="0" posthx="40" posthy="0"/>')
        file.write('                            <key value="549" frame="' +str(diffValue)+ '" type="0" prehx="-40" prehy="0" posthx="40" posthy="0"/>')
        file.write('                        </field>')
    else:
        file.write(line)
        file.write('\n')
file.close()
