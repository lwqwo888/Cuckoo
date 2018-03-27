# coding=utf-8
import os
import json
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


a = {
    'a':[
        [1,2,3,4,5],
        [1,2,3,4,5],
        [1,2,3,4,5],
        [1,2,3,4,5],
    ]
}


print a
x = 1
for i in a:
    n = 0
    for j in a[i]:
        if n >= x:
            print j
        n = n +1