# coding=utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

list3 = ['金色 4+32 全网通','黑色 4+32 全网通','玫瑰金 4+32 全网通','金色 4+64 全网通','黑色 4+64 全网通','玫瑰金 4+64 全网通','红色限量版 4+64']
list4 = ['官方标配']
list5 = ['64GB']
list6 = ['中国大陆']

s_list=[list3,list4,list5,list6]

# list1 = ['S','M','L','XL','XXL']
# list2 = ['黑色','海沫蓝','贝壳粉','白色','灰色','中国红']
#
# s_list=[list1, list2]
s=""

def division(s,n):

    if n == -1:
        return s # 递归特性一：必须有一个明确的结束条件
    else:
        str_list=[]
        if isinstance(s,list):
            for i in s_list[n]:
                for j in s :
                    s_sum=i+j
                    str_list.append(s_sum)
                    # print(str_list)
        else:
            for i in s_list[n]:
                s_sum = i
                str_list.append(s_sum)
        n=n-1
        s=str_list


        return division(s,n)  # 递归特性而：每次递归都是为了让问题规模变小


s=division(s,3)  # 递归特性三：递归层次过多会导致栈溢出，且效率不高

for i in s:
    print i
