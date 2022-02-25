# -*- coding: utf-8 -*-
"""
Created on Thu Feb 24 12:13:16 2022

@author: Лена
"""

import re
import numpy as np
#import collections
import subprocess
#import math

st = '{"query": {"bool": {"must": [{"multi_match": {"query": "COVID","fields": ["textBody", "title"]}}]}}}'
st = re.sub('"', '\\"', st)

response = subprocess.run(
    'C:/curl/curl-7.81.0-win64-mingw/bin/curl.exe -X GET \"http://localhost:9200/_all/_search?pretty=true&size=100\" -H \"Content-Type: application/json\" -d ' + f'"{st}"',
  capture_output=True, shell=True
)
#print(response)

#Декодуємо та форматуємо відповідь
filtered_data = response.stdout.decode('utf-8')
json =filtered_data.split('\n')
t=""
for i in range(len(json)):
    t=t+" "+json[i]
title = re.findall('"title" : "(.+?)"source"', t)
t=""
for i in range(len(title)):
    t=t+" "+title[i]

t=re.sub('"textBody" :','.',t)
t=re.sub('[-–%―‖[\]\/0-9",()$+»«—:;_…]',' ',t)
t=t.upper()
sent =t.split('.')
f = open("words.txt","r")
t = f.read()
f.close()
t=t.upper()
w =t.split('\n')
for i in range(len(w)):
    s =w[i].split(' ')
    w[i]=s[-1]
mtr = np.eye(len(w))
for i in range(len(w)):
    mtr[i][i]=0

stroka=""
for i in range(len(w)):
    stroka=stroka+";"+w[i]
    
    
for i in range(len(sent)):
    for j in range(len(w)):
        for k in range(len(w)):
            if(j!=k):
                if (re.search(w[j],sent[i])):
                    if (re.search(w[k],sent[i])):
                        mtr[k][j]=mtr[k][j]+1

f=open("concept.csv","w")
f.write(stroka+"\n")
for i in range(len(w)-1):
    f.write(w[i]+";") 
    for j in range(len(w)-1):
        f.write(str(mtr[i][j])+";") 
    f.write("\n")
f.close()