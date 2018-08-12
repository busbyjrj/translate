import requests
import hashlib
import random
import json
import re
import sys
import time

def get_content():
    '''
    处理PDF文件复制后多余的换行
    '''
    print('请输入要翻译的内容：')
    transText = ""
    line = sys.stdin.readline()
     
    while line != "#\n":
            transText += line
            line = sys.stdin.readline()

    transText = transText.replace(".\n","段落")
    transText = transText.replace("\n"," ")
    transText = transText.replace("段落","\n")

    pattern = re.compile(r'\n[A-Z]')
    res = pattern.findall(transText)

    for i in res:
        transText = transText.replace(str(i),'\n'+str(i)[1])

    transText = transText.split('\n')

    for each in transText:
        get_translation(each)


def get_translation(q):
    '''
    调用百度翻译Api实现翻译
    '''
    appid = '百度翻译appid'
    secretKey = '百度翻译secreKey'

    url = 'https://fanyi-api.baidu.com/api/trans/vip/translate'

    try:
        compile_trans = re.compile(r'(^[\u4e00-\u9fa5]{0,}$)')
        if compile_trans.match(q):
            from_ = 'zh'
            to_ = 'en'
        else:
            from_ = 'en'
            to_ = 'zh'
        salt = random.randint(32768, 65536)

        sign = (appid + q + str(salt) + secretKey).encode("utf-8")
        m1 = hashlib.md5(sign)
        sign = m1.hexdigest()

        data = {
            'q' : q,
            'from' : from_,
            'to' : to_,
            'appid' : appid,
            'salt' : salt,
            'sign' : sign,}

        res = requests.post(url, data).text

        target = json.loads(res)

        print(target['trans_result'][0]['dst']+'\n\n\n')
    except:
        pass

while True:
    get_content()

