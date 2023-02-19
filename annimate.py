#!/opt/homebrew/opt/python@3.9/libexec/bin/python

from operator import inv
import re

ofile=open('Dwadasha-new.ove', encoding='utf-8')
olines=ofile.read().splitlines()
ofile.close()

TAMIL_TRACK=1
SANSKRIT_TRACK=-5

file=open('Dwadasha-animate.ove', 'w', encoding='utf-8')
titleBlock=False
transformBlock=False
posxBlock=False
posyBlock=False
writeLine=True
for line in olines:
    writeLine=True
    if "Title" in line:
        titleBlock=True
        rr=re.search(r"track=\"((-)?\d+)\"",line)
        trackNumber=int(rr.group(1))
        rr=re.search(r"in=\"(\d+)\" out=\"(\d+)\"",line)
        inValue = int(rr.group(1))
        outValue = int(rr.group(2))
        diffValue = outValue - inValue
        #print("%d - %d = %d" %(outValue, inValue, diffValue))
    if "</clip>" in line:
        titleBlock=False
    if titleBlock and "Distort/Transform" in line:
        transformBlock=True
    if "</effect>" in line:
        transformBlock=False
    if titleBlock and transformBlock and "posx" in line:
        posxBlock=True
    if titleBlock and transformBlock and "posy" in line:
        posyBlock=True
    #print("titleBlock=%s transformBlock=%s posxBlock=%s posyBlock=%s line=%s" %(titleBlock, transformBlock, posxBlock, posyBlock, line))
    if titleBlock and transformBlock and posxBlock:
        if trackNumber == TAMIL_TRACK:
            file.write('                        <field id="posx" value="-640">\n')
            file.write('                            <key value="-640" frame="0" type="0" prehx="-40" prehy="0" posthx="40" posthy="0"/>\n')
            file.write('                            <key value="640" frame="10" type="0" prehx="-40" prehy="0" posthx="40" posthy="0"/>\n')
            file.write('                            <key value="640" frame="'+str(diffValue-11)+'" type="0" prehx="-40" prehy="0" posthx="40" posthy="0"/>\n')
            file.write('                            <key value="1920" frame="'+str(diffValue-1)+'" type="0" prehx="-40" prehy="0" posthx="40" posthy="0"/>\n')
            file.write('                        </field>\n')
            writeLine=False
        elif trackNumber == SANSKRIT_TRACK:
            file.write('                        <field id="posx" value="1920">\n')
            file.write('                            <key value="1920" frame="0" type="0" prehx="-40" prehy="0" posthx="40" posthy="0"/>\n')
            file.write('                            <key value="640" frame="10" type="0" prehx="-40" prehy="0" posthx="40" posthy="0"/>\n')
            file.write('                            <key value="640" frame="'+str(diffValue-11)+'" type="0" prehx="-40" prehy="0" posthx="40" posthy="0"/>\n')
            file.write('                            <key value="-640" frame="'+str(diffValue-1)+'" type="0" prehx="-40" prehy="0" posthx="40" posthy="0"/>\n')
            file.write('                        </field>\n')
            writeLine=False
        posxBlock=False
    if titleBlock and transformBlock and posyBlock:
        if trackNumber == TAMIL_TRACK:
            file.write('                        <field id="posy" value="340">\n')
            file.write('                            <key value="340" frame="0" type="0" prehx="-40" prehy="0" posthx="40" posthy="0"/>\n')
            file.write('                            <key value="340" frame="10" type="0" prehx="-40" prehy="0" posthx="40" posthy="0"/>\n')
            file.write('                            <key value="340" frame="'+str(diffValue-11)+'" type="0" prehx="-40" prehy="0" posthx="40" posthy="0"/>\n')
            file.write('                            <key value="340" frame="'+str(diffValue-1)+'" type="0" prehx="-40" prehy="0" posthx="40" posthy="0"/>\n')
            file.write('                        </field>\n')
            writeLine=False
        elif trackNumber == SANSKRIT_TRACK:
            file.write('                        <field id="posy" value="370">\n')
            file.write('                            <key value="370" frame="0" type="0" prehx="-40" prehy="0" posthx="40" posthy="0"/>\n')
            file.write('                            <key value="370" frame="10" type="0" prehx="-40" prehy="0" posthx="40" posthy="0"/>\n')
            file.write('                            <key value="370" frame="'+str(diffValue-11)+'" type="0" prehx="-40" prehy="0" posthx="40" posthy="0"/>\n')
            file.write('                            <key value="370" frame="'+str(diffValue-1)+'" type="0" prehx="-40" prehy="0" posthx="40" posthy="0"/>\n')
            file.write('                        </field>\n')
            writeLine=False
        posyBlock=False
    if writeLine:
        file.write(line)
        file.write('\n')
file.close()
