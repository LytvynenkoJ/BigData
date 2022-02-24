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

filtered_data = response.stdout.decode('utf-8')

json =filtered_data.split('\n')
t=""
for i in range(len(json)):
    t=t+" "+json[i]

title = re.findall('"title" : "(.+?)"source"', t)
t=""
for i in range(len(title)):
    t=t+" "+title[i]

#Зберігаємо текст кожного знайденого документу
text=[]
words=[]
for i in range(len(title)):
    text.append(re.sub('"textBody" :','',title[i]))
    #Замінюємо всі можливі "не слова" на символ пробілу
    text[i]=re.sub('[---‖[\]\/?0-9",.()$+»«—:;_…<>%#&]',' ', text[i])
    text[i]=text[i].upper()
    text[i]=re.sub('\s\w\s',' ',text[i])
    text[i]=re.sub('\s\w\w\s',' ',text[i])
    text[i]=re.sub('\s\s+',' ',text[i])
    words.append(text[i].split(' '))


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

def compute_tf(text):
    #На вход берем текст в виде списка (list) слов
    #Считаем частотность всех терминов во входном массиве с помощью 
    #метода Counter библиотеки collections
    tf_text = collections.Counter(text)
    for i in tf_text:
        #для каждого слова в tf_text считаем TF путём деления
        #встречаемости слова на общее количество слов в тексте
        tf_text[i] = tf_text[i]/float(len(text))
    #возвращаем объект типа Counter c TF всех слов текста
    return tf_text

computed_tf=compute_tf(word)

def compute_idf(w, corpus):
    #на вход берется слово, для которого считаем IDF
    #и корпус документов в виде списка списков слов
    #количество документов, где встречается искомый термин
    #считается как генератор списков
    if sum([1.0 for i in corpus if w in i])!=0:
        return math.log10(len(corpus)/sum([1.0 for i in corpus if w in i]))
    else:
        del computed_tf[w]

d={}
print()
for i in word:
    d[i]=compute_idf(i,words)
    
print(d)

documents_list = []

for text in words:
    tf_idf_dictionary = {}
    computed_tf = compute_tf(text)
    for w in computed_tf:
        tf_idf_dictionary[w] = computed_tf[w] * compute_idf(w, words)
    documents_list.append(tf_idf_dictionary)

print(documents_list[0])

#Виключаємо з отриманого словника стоп-слова та виводимо М найважливіших слів
#для кожної новини
f = open("stop_words.txt","r")
t = f.read()
f.close()
t=t.upper()
stop=t.split(' ')
M=5
f = open("tf_idf_words.csv","w")
f.write("news№;word№;word;value\n")
for k in range(len(documents_list)):
    j=1
    sorted_dict = {}
    sorted_keys = sorted(documents_list[k], key=documents_list[k].get, reverse=True) # [1, 3, 2]
    for w in sorted_keys:
        sorted_dict[w] = documents_list[k][w]
        pr=0
        #Перевіряємо чи наше слово є стоп-словом
        for i in range(len(stop)):
            if (stop[i] == w):
                pr=1
        #Якщо ні, то виводимо на екран
        if (pr == 0):
            f.write(str(k)+";"+ str(j) + ";" + w + ";"+ str(sorted_dict[w])+"\n")
            print(k,j,w,sorted_dict[w])
            j=j+1
        #Якщо вже вивели М слів, то зупиняємось
        if (j > M):
            f.write(";;;\n")
            break

f.close()    
