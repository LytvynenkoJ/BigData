# -*- coding: utf-8 -*-
"""
Created on Wed Feb 23 10:09:31 2022

@author: Лена
"""

#!/usr/bin/python2.7
import re
import subprocess

st = '{"query":{"multi_match":{"query":"COVID","fields":["textBody","title"]}},"aggregations":{"dates_with_holes":{"date_histogram":{"field":"PubDate","calendar_interval":"1d","min_doc_count":0}}},"size":0}'
st = re.sub('"', '\\"', st)

response = subprocess.run('C:/curl/curl-7.81.0-win64-mingw/bin/curl.exe -X GET \"http://localhost:9200/_all/_search?pretty=true\" -H \"Content-Type: application/json\" -d ' + f'"{st}"',capture_output=True, shell=True)                                                  
print(response.stdout)
filtered_data = response.stdout.decode('utf-8')

json =filtered_data.split('\n')

t=""
for i in range(len(json)):
    t=t+" "+json[i]
t=re.sub('^\s','',t)
days = re.findall('"key_as_string" : "(.+?)T', t)
count = re.findall('"doc_count" : (\d+)', t)

file = open("dates_docs.csv", "w", encoding='utf-8')
for i in range(len(days)):
    print(days[i]+";"+count[i])
    file.write(days[i]+";"+count[i]+"\n")
file.close()