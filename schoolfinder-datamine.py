#!/opt/homebrew/opt/python@3.9/libexec/bin/python

import glob
import json
import re

files=sorted(glob.glob("/Users/rajaramaniyer/Downloads/schools/*.html"))
# files=glob.glob("/Users/rajaramaniyer/Downloads/schools/singapore-sports-school.html")

schools=[]
for filename in files:
    print('Processing '+filename)
    file = open(filename, 'r', encoding="UTF-8")
    data = file.read()
    file.close()
    data=re.sub(r'(.*\n)+(\s+<h1 class="m-b:l">)', r'\2', data)
    data=re.sub(r'(\s+)?</main>(\n.*)+', '', data)
    data=re.sub(r'<li>([^<]+)\n', r'<li>\1', data)
    data=re.sub(r'<div><a[^<]+href="https://.*goo[^"]+"[^>]+>(.*)</a></div>', r'"SchoolAddress": "\1",', data)
    data=re.sub(r'(\s+)?<span[^>]+>Email:</span>\n(\s+)?<a[^<]+href="mailto[^"]+"[^>]+>(.*)</a>', r'\n"Email": "\3",', data)
    data=re.sub(r'(\s+)?<span[^>]+>Website:</span><a[^>]+>(http.*)</a>.*',r'\n"Website": "\2",',data)
    data=re.sub(r'<a[^<]+href="([^"]+)"([^>]+)?>[^<]*</a>',r'\1',data)
    data=re.sub(r'><',r'>\n<',data)
    data=re.sub(r'<',r'\n<',data)
    data=re.sub(r'\n\s+',r'\n',data)
    data=re.sub(r'\s+\n',r'\n',data)
    data=re.sub(r'<.*?>\n','',data)
    data=re.sub(r'<span>(.*)\n',r'"SchoolArea": "\1",\n',data)
    data=re.sub(r'<h1 class="m-b:l">(.*)\n',r'{\n"SchoolName": "\1",\n',data)
    data=re.sub(r'<span class="ts:m c:grey-2 m-l:xs">(School code([^:]+)?):\n<span class="fw:7">(\d+)\n', r'"\1": "\3",\n', data)
    data=re.sub(r'<li>(.*)\n', r'"\1",\n', data)
    data=re.sub(r'<span class="moe-collapsible__heading">(.*)\n', r'], "\1": [\n', data)
    data=re.sub(r'<th>(Non-)?[aA]ffiliated\n',r'',data)
    data=re.sub(r'.*Empty table header\n',r'',data)
    data=re.sub(r'</i>Visit the school website to learn more.\n', r'],\n', data)
    data=re.sub(r'<span class="ff:heading ts:xl fw:6 c:grey-1">(About|Contact)\n',r'',data)
    data=re.sub(r'<span class="ff:heading ts:xl fw:6 c:grey-1">(.*)\n', r'"\1": [\n', data)
    data=re.sub(r'<span class="d:b m-b:s">(.*)\n', r'"\1",\n', data)
    data=re.sub(r'<span class="d:b fw:7 c:grey-2">(.*):\n<span class="d:b c:grey-2( m-b:l)?">(.*)\n', r'"\1": "\3",\n', data)
    data=re.sub(r'<span class="d:b ff:heading ts:l m-b:m fw:6 c:grey-1 ">(.*)\n', r'"\1",\n', data)
    data=re.sub(r'<span class="d:b ts:m m-b:m fw:7 c:grey-2">(.*)\n', r'"\1",\n', data)
    data=re.sub(r'\n.*PSLE score range of 2021.*\n','\n',data)
    data=re.sub(r'\nHCL Grade.*\n',r'\n',data)
    data=re.sub(r'<th>(.*)\n<p>(.*)\n<p>(.*)\n', r'"\1-Affliated": "\2",\n"\1-Non-affliated": "\3",\n', data)
    data=re.sub(r'<p class="d:b ff:body ts:s fs:i m-t:l".*?>(.*)\n(\],)?', r'"Note": "\1",\n', data)
    data=re.sub(r'\], "Subjects offered": \[','"Subjects offered": [',data)
    data=re.sub(r'<strong>Note:(\n[^"]*)+','',data)
    data=re.sub(r'<p class="m-b:xl">(.*)\n', r'', data)
    data=re.sub(r'</div>','}',data)
    data=re.sub(r',\n([]}])',r'\n\1',data)
    data=re.sub(r'\n"(.*)",\n"School mode"', r'"\1"\n],\n"School mode"', data)
    data=re.sub(r'&nbsp;', r' ', data)
    data=re.sub(r'\n\*(.*)\n', r'"Note": "\1",\n', data)
    with open(filename.replace('.html','.json'), "w") as file:
        file.write(data)
    schools.append(json.loads(data))
with open('secondary-schools.json', "w") as file:
    json.dump(schools, file, indent=2)
