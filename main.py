# -*- coding: utf-8-*-
import urllib.parse
import urllib.request
import json
import random
import math
import os

# 影响因素url：详见巨潮资讯API文档：http://webapi.cninfo.com.cn/#/apiDoc
factor_url = "http://webapi.cninfo.com.cn/api/stock/p_stock2303"
values = {'status': 'hq', 'token': 'C6AD7DAA24BAA29AE14465DDC0E48ED9'}

# 对请求数据进行编码
data = urllib.parse.urlencode(values).encode('utf-8')
print(type(data))   # 打印<class 'bytes'>
print(data)         # 打印b'status=hq&token=C6AD7DAA24BAA29AE14465DDC0E48ED9'

# 若为post请求以下方式会报错TypeError: POST data should be bytes, an iterable of bytes, or a file object. It cannot be of type str.
# Post的数据必须是bytes或者iterable of bytes,不能是str,如果是str需要进行encode()编码
data = urllib.parse.urlencode(values)
print(type(data))   # 打印<class 'str'>
print(data)         # 打印status=hq&token=C6AD7DAA24BAA29AE14465DDC0E48ED9

# 将数据与url进行拼接
req = factor_url + '?' + data
# 打开请求，获取对象
response = urllib.request.urlopen(req)
print(type(response))  # 打印<class 'http.client.HTTPResponse'>
# 打印Http状态码
print(response.status) # 打印200
# 读取服务器返回的数据,对HTTPResponse类型数据进行读取操作
the_page = response.read()
# 中文编码格式打印数据
print(the_page.decode("unicode_escape"))

# # 资产报酬率=息税前利润/平均资产总额 F016N:总资产报酬率
# # 净资产收益率=ROE=净利润/净资产
# # 营业净利率=净利润/营业收入
# # 流动比率=流动资产/流动负债
# # 速动比率=速动资产/流动负债
# # 资产负债率=负债总额/资产总额
# # 保守速动比率=(现金+ 短期证券+ 应收票据+应收账款净额) / 流动负债，-----缺括号里的全部
# # 现金比率=（货币资金+有价证券）/流动负债，-----缺有价证券
# 应收账款周转率=
# 存货周转率   F023N
# # 流动资产周转率=主营业务收入净额/平均流动资产总额，平均流动资产总额=（流动资产年初数+流动资产年末数）/2
# # 固定资产周转率=营业收入 / 平均固定资产净值，固定资产平均净值=(期初净值+期末净值)÷2
# 总资产周转率=销售收入/总资产，营业成本么
# # 总资产增长率=本年总资产增长额/年初资产总额
# # 营业收入增长率=(营业收入增长额/上年营业收入总额)
# 每股收益
# 每股现金净流量
# 每股营业收入
# 每股净资产