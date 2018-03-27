# coding=utf-8
# 通过html抓取商品尺码和颜色和PVS

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class PVS(object):
    def __commodity_pvs(self, s, n, big_list):

        if n == -1:
            return s
        else:
            str_list = []
            if isinstance(s, list):
                for i in big_list[n]:
                    for j in s:
                        s_sum = i + '|' + j
                        str_list.append(s_sum)
            else:
                for i in big_list[n]:
                    s_sum = i
                    str_list.append(s_sum)
            s = str_list
            n = n - 1
            return self.__commodity_pvs(s, n, big_list)

    def pvs(self, count, big_list, dict):
        list = []
        s = ''
        # 商品属性列表
        Product_attributes_list = self.__commodity_pvs(s, count-1, big_list)

        for i in Product_attributes_list:
            single_commodity_list = i.split('|')
            pvs_string = ''
            for j in single_commodity_list:
                str = dict[j] + ';'
                for x in range(len(str)):
                    pvs_string += str[x]
            list.append(pvs_string)
        return Product_attributes_list, list