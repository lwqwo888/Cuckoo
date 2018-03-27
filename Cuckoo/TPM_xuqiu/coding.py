# coding=utf-8
import chardet
from Queue import Queue
import sys
reload(sys)
sys.setdefaultencoding('utf-8')



str1 = "788 ถ.ประชาราษฎร์สาย1 แขวงบางซื่อ เขตบางซื่อ กทม."
str2 = " 132/3 ม.10ต.โพรงมะเดื่อ อ.เมือง จ.นครปฐม  "
print chardet.detect("788 ถ.ประชาราษฎร์สาย1 แขวงบางซื่อ เขตบางซื่อ กทม.")
print chardet.detect(''' 132/3 ม.10ต.โพรงมะเดื่อ อ.เมือง จ.นครปฐม  ''')
n_str1 = str1.decode("unicode-escape")
print str1.decode("gbk").encode("utf-8")
print n_str1
# print chardet.detect(n_str1)
print "Shipment Delivered" == "Shipment Delivered"