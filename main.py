# -*- coding: utf-8-*-
import json
import os
import requests

# 以下两个api请输入您在巨潮资讯->个人中心查询到的key和secret
access_key = "Oy0UB0fDAg87iKCaRg0zMQr59pDG9jF"
access_secret = "ATg1ZqRt4Y9OSQsCAqNxRHzZpfhsfVMs"
# 影响因素url：详见巨潮资讯API文档：http://webapi.cninfo.com.cn/#/apiDoc
factor_url = "http://webapi.cninfo.com.cn/api/stock/p_stock2303"
# 因为巨潮资讯的API一次最多只能返回50个企业的数据，故请将需要查询企业的代码分批次存在


def get_code_txt(txt_path):
    with open(txt_path, 'r+', encoding='utf-8') as file:
        output = ""
        for i in file.readlines():
            output += i
            output += ','
    # 后验检测是否超过50个企业
    if len(output) > 399:
        print("请检查输入企业数量，检测到超出50家，建议直接从巨潮资讯复制，而不是手动输入")
        raise SystemExit
    return output


# 用于获取token，这块是巨潮资讯Doc中的方法
def gettoken(client_id, client_secret):
    token_url = 'http://webapi.cninfo.com.cn/api-cloud-platform/oauth2/token'
    post_data = "grant_type=client_credentials&client_id=%s&client_secret=%s" % (client_id, client_secret)
    post_data = {"grant_type": "client_credentials",
               "client_id": client_id,
               "client_secret": client_secret
               }
    req = requests.post(token_url, data=post_data)
    tokendic = json.loads(req.text)
    return tokendic['access_token']


def get_fifty_enterprise(enterprise_number_txt_path: str, csv_save_path: str, flag: bool):
    code = get_code_txt(enterprise_number_txt_path)

    # 需要获取的参数，只能用逗号隔开
    need = "ORGNAME,SECCODE,SECNAME,STARTDATE,ENDDATE,F016N,F014N,F101N,F089N,F042N,F043N," \
           "F041N,F049N,F044N,F022N,F023N,F029N,F026N,F025N,F056N,F052N,F003N,F008N"
    # 请求参数
    values = {"scode": code.replace('\n', '').replace('\r', '')[:-1],
              "source": "033003",
              "format": "csv",
              "sdate": "2019-01-01",
              "edate": "2019-12-31",
              "rdate": "2019-12-31",
              "@column": need,
              "@orderby": "id:asc",
              # "@limit": "1",
              }
    token = gettoken(access_key, access_secret)
    # 附上加密部分，形成最终url
    url = factor_url + '?subtype=001&access_token=' + token
    response = requests.post(url=url, data=values)
    # # 打印状态码
    # print(response.status_code)
    # # 打印返回数据
    # print(response.text)
    if flag:
        # 因为返回csv的格式，所以这一段是为了去除自带的那段神秘排序完的header，通过换行符来搜索
        delete_str = response.text.split("\n")[0] + "\n"
        # 删掉第一行
        data = response.text.replace(delete_str, "")
        with open(csv_save_path, "a") as f:
            f.write(data)
            print("写入成功：%s" % csv_save_path)
    else:
        with open(csv_save_path, "a") as f:
            f.write(response.text)
            print("写入成功：%s" % csv_save_path)


if __name__ == '__main__':
    csv_save_dir = "csv_save_dir/"
    enterprise_number_dir = "enterprise_number/"
    enterprise_number_txt = enterprise_number_dir + "code_1.txt"
    csv_save = csv_save_dir + "data.csv"

    # # 只读一个txt里的，追加写入
    # get_fifty_enterprise(enterprise_number_txt, csv_save, flag=False)

    # 遍历读文件夹内所有的txt，每个只能存50个企业代码，追加写入
    txt_file = os.listdir(enterprise_number_dir)
    for i in range(len(txt_file)):
        if i == 0:
            get_fifty_enterprise(enterprise_number_dir + txt_file[i],
                                 csv_save, flag=False)
        else:
            get_fifty_enterprise(enterprise_number_dir + txt_file[i],
                                 csv_save, flag=True)
