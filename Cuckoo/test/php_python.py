#!/usr/bin/env python
#coding=utf-8
import os
file=open("redis_list.txt", "r")
file_content=file.read()
php_array=file_content.replace("'normal' => array(","")
pstr = php_array.replace(" ","").replace("\r","").replace("\n", "").replace("\t", "").replace("(", "").replace("'", "").replace("),", "")
#print pstr
pstr_list = pstr.split("redis_list=>array")
#print type(pstr_list)

cf_param = []
for i in pstr_list:
 if i:
  ## 'host'=>'127.0.0.1','port'=>6411,'db'=>2
  i_list = i.split(",")
  if len(i_list)==3:
   op = {}
   for ii in i_list:
    ii_list = ii.split("=>")
    if len(ii_list) == 2:
     op[ii_list[0]] = ii_list[1]
   cf_param.append(op)

for i in cf_param:
    print "redis -h "+i["host"] + " -p "+i["port"] +"|select" +" "+i["db"]