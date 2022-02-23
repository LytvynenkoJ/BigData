# -*- coding: utf-8 -*-
"""
Created on Sun Feb 20 17:03:16 2022

@author: Лена
"""

#!/usr/local/bin/python2.7
import re
import json
import cgi
import subprocess
form = cgi.FieldStorage()
query = form.getfirst("query", "")
src = form.getfirst("src", "")

if query!="" and src!="":
    st = '{{"query": {{"bool": {{"must": [{{"multi_match": {{"query": {},"fields": ["textBody", "title"]}}}}],"filter": [{{"match": {{"source": {}}}}}]}}}}}}'.format(
    json.dumps(query), json.dumps(src))
if query!="" and src=="":
    st = '{{"query": {{"bool": {{"must": [{{"multi_match": {{"query": {},"fields": ["textBody", "title"]}}}}],"filter": []}}}}}}'.format(
    json.dumps(query))
if query=="" and src!="":
    st = '{{"query": {{"bool": {{"filter": [{{"match": {{"source": {}}}}}]}}}}}}'.format(
    json.dumps(src))
if query=="" and src=="":
    st = '{{"query": {{"bool": {{"must": [],"filter": []}}}}}}'


st = re.sub('"', '\\"', st)

response = subprocess.run(
    'C:/curl/curl-7.81.0-win64-mingw/bin/curl.exe -X GET \"http://localhost:9200/_all/_search?pretty=true&size=100\" -H \"Content-Type: application/json\" -d ' + f'"{st}"',
  capture_output=True, shell=True
)


filtered_data = response.stdout.decode('utf-8')

json =filtered_data.split('\n')
t=""
for i in range(len(json)):
    t=t+" "+json[i]
t=re.sub('^\s','',t)
total = re.findall('\"took\" : (\d+),', t)
title = re.findall('"title" : "(.*?)",', t)
text = re.findall('"textBody" : "(.*?)",', t)
url = re.findall('"URL" : "(.*?)"', t)
print("Content-type:text/html\r\n\r\n")
print("<html>")
print("<head>")
print('<meta http-equiv="Content-Type" charset=utf-8" />')
print("</head>")
print ("<body bgcolor=#ccffff>")
print ("<b>Found: "+str(len(title))+"</b><hr><ol>")
for i in range(len(title)):
    doc_ind=i+1
    print ("<li><b>"+": "+title[i]+"</b>")
    print ("<br>"+text[i])
    print ("<br><i>"+url[i]+"</i><br /><hr>")
print ("</ol></body></html>")