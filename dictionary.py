# -*- coding: utf-8 -*-
"""
Created on Thu Feb 24 12:13:16 2022

@author: Лена
"""

import re
import collections
import subprocess
import math

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

#Замінюємо всі можливі "не слова" на символ пробілу
t=re.sub('"textBody" :','',t)
t=re.sub('[-–―‖[\]\/?0-9",.()$+»«—:;_…<>%#&]',' ',t)
t=t.upper()
t=re.sub('\s\w\s',' ',t)
t=re.sub('\s\w\w\s',' ',t)
t=re.sub('\s\s+',' ',t)
#Розбиваємо отриманий текст на слова та сортуємо їх
word =t.split(' ')
word.sort()
#Формуємо словник
d={}
old=""
n=0;
for i in range(len(word)):
    if (word[i] == old):
        n=n+1;
    else:
        d[old]=n
        old=word[i]
        n=1
d[old]=n

sorted_dict = {}
sorted_keys = sorted(d, key=d.get, reverse=True)
for w in sorted_keys:
    sorted_dict[w] = d[w]
    
#Позбавляємося від стоп-слів у словнику та виводимо М найвживаніших слів
f = open("stop_words.txt","r")
t = f.read()
f.close()
t=t.upper()
stop =t.split('\n')
M=20
j=1
sorted_dict = {}
sorted_keys = sorted(d, key=d.get, reverse=True)
f = open("dict.csv","w")
f.write("№;word;number\n")
for w in sorted_keys:
    sorted_dict[w] = d[w]
    pr=0
    for i in range(len(stop)):
        if (stop[i] == w):
            pr=1
    if (pr == 0):
        f.write(str(j)+";" +w+";" +str(sorted_dict[w])+"\n")
        print(j,w,sorted_dict[w])
        j=j+1
    if (j > M):
        break
f.close()