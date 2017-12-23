# coding=utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
str='G20-放假安排'
result = str.split('-')[1:][0]
print(result)