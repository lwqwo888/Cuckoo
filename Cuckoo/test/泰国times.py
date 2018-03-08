# coding=utf-8
# 免责声明: 此代码是为快捷查询由刘文强编写的,与服务器上其他工程师编写的泰国times(taiguo_api2_final.py)代码稍有不同.
import requests
import json
from collections import OrderedDict
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


try:
    url = 'http://stg.timesoms.com/api/orders/THCUC05103644'
    headers = {
        "Authorization": "Bearer sbv99QoVncfr4twUlpByLwGLNKMMfLlSKtU0DIZYGFl85o5SlWeMvsShlIvl"
    }
    params = {
        'token': 'fJ83StsDzZPI50N0yksVUdaBVZIxR3FZqS4pKmG3yK2YQBVGQC0Pz7vNRuz0'
    }
    res = requests.get(url, headers=headers, params=params).text
    print res
    dict = json.loads(res)
    if 'milestones' in res:
        taiguo_keys = json.loads(res, object_pairs_hook=OrderedDict)['milestones'].keys()
        taiguo_values = json.loads(res, object_pairs_hook=OrderedDict)['milestones'].values()
        list = []
        i = 0

        for taiguo_key in taiguo_keys:
            if taiguo_values[i]:
                list.append(taiguo_values[i] + "  " + taiguo_keys[i])
                # print '%s --- %s' % (taiguo_values[i], taiguo_keys[i])
            i = i + 1
        list1 = sorted(list)
        for v in list1:
            print v

    else:
        print "未上线"

except Exception as e:
    print e

