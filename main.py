# -*- coding: utf-8-*-
import json
import urllib
import requests
import datetime




def get_code_txt(txt_path):
    with open(txt_path, 'r+', encoding='utf-8') as f:
        output = ""
        for i in f.readlines():
            print(i)
            output += i[:-1]
            output += ','
    return output


# 用于获取token
def gettoken(client_id,client_secret):
    url = 'http://webapi.cninfo.com.cn/api-cloud-platform/oauth2/token'
    post_data = "grant_type=client_credentials&client_id=%s&client_secret=%s" % (client_id, client_secret)
    post_data = {"grant_type": "client_credentials",
               "client_id": client_id,
               "client_secret": client_secret
               }
    req = requests.post(url, data=post_data)
    tokendic = json.loads(req.text)
    return tokendic['access_token']


# 用于解析接口返回内容
def getPage(url):
    response = urllib.request.urlopen(url)
    return response.read().decode('utf-8')


if __name__ == '__main__':
    access_key = "Oy0UB0fDAg87iKCaRg0zMQr59pDG9jFz"
    access_secret = "ATg1ZqRt4Y9OSQsCAqNxRHzZpfhsfVMP"
    # 影响因素url：详见巨潮资讯API文档：http://webapi.cninfo.com.cn/#/apiDoc
    factor_url = "http://webapi.cninfo.com.cn/api/stock/p_stock2303"
    # 股票代码
    code = "600004"
    # 需要获取的参数，只能用逗号隔开
    need = "ORGNAME,SECCODE,SECNAME,STARTDATE,ENDDATE,F016N,F014N,F042N,F043N," \
           "F041N,F049N,F044N,F022N,F023N,F029N,F026N,F025N,F056N,F052N,F003N,F008N"
    # 请求参数
    values = {"scode": code,
              "source": "033003",
              "format": "json",
              "sdate": "2019-01-01",
              "edate": "2019-12-31",
              "rdate": "2019-12-31",
              "@column": need,
              "@orderby": "id:asc",
              "@limit": "1",
              }
    token = gettoken(access_key, access_secret)  ##请在平台注册后并填入个人中心-我的凭证中的Access Key，Access Secret
    # url = factor_url + '&access_token=' + token
    url = 'http://webapi.cninfo.com.cn/api/stock/p_stock2303?subtype=001&access_token=' + token
    print(token)
    print(url)
    # result = json.loads(getPage(url))
    # print()
    # for i in range(1):
    #     print(result['records'][i]['PARENTCODE'], result['records'][i]['SORTCODE'], result['records'][i]['SORTNAME'],
    #           result['records'][i]['F002V'])
    #
    # response = requests.post(url=url, data=values)
    # print(response.text)
    # print(type(response.text))
    a = get_code_txt("code.txt")
    print(a)
    # print(response.status_code)
    # print(response.url)
    # print(response.json())
