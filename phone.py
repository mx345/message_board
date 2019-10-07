# import urllib.parse
import urllib.request
import requests
import json
import sys
import random
verify_code = str(random.randint(100000, 999999))
phone = "17371290626"
host = 'http://toushitz.market.alicloudapi.com'
path = '/ts/notifySms'
method = 'POST'
appcode = '4c02b58aaeab4b36abeef070f70fe1d4'
querys = 'mobile=17371290626&param=#code#=123456&tpl_id=TP1910072'
bodys = {}
url = host + path + '?' + querys

request1 =  urllib.request.Request(url)
request1.add_header('Authorization', 'APPCODE ' + appcode)
response = urllib.request.urlopen(request1)
print(response)
content = response.read()

if (content):
    print(content)


# def send_sms_code(phone):
#     '''
#     函数功能：发送短信验证码（6位随机数字）
#     函数参数：
#     phone 接收短信验证码的手机号
#     返回值：发送成功返回验证码，失败返回False
#     '''
#     verify_code = str(random.randint(100000, 999999))

#     try:
#         url = "http://toushitz.market.alicloudapi.com/ts/notifySms"
#         params = {
#             "mobile": phone,  # 接受短信的用户手机号码
#             "tpl_id": "TP1910072",  # 您申请的短信模板ID，根据实际情况修改
#             "tpl_value": "#code#=%s" % verify_code,  # 您设置的模板变量，根据实际情况修改
#             "key": "4c02b58aaeab4b36abeef070f70fe1d4",  # 应用APPKEY(应用详细页查询)
#         }
#         params = urllib.parse.urlencode(params).encode()

#         f = urllib.request.urlopen(url, params)
#         content = f.read()
#         res = json.loads(content)
#         print(res)
#         print(verify_code)
#         if res and res['error_code'] == 0:
#             # if not res :
#             return False
#         else:
#             return verify_code
#     except:
#         return False


# send_sms_code(phone)
