#coding=utf-8
__author__ = 'zxlee'
__github__ = 'https://github.com/SmileZXLee/MaHuaFilmGetTool'

import json
import requests
from requests.cookies import RequestsCookieJar
import urllib
from pyDes import *
import base64
import re

des_Key = "s!u03#sa" # Key
def json_dic(json_str):
	try:
		json_object = json.loads(json_str)
	except Exception as err:
		json_object = {}
	return json_object

def get_req(url):
	up = urllib.parse.urlparse(url)
	conn = httplib.HTTPConnection(up.netloc)
	conn.request(method="GET",url=url) 
	response = conn.getresponse()
	res= response.read()
	return res;


def send_req(url,headers,data,post_type):
	str_json = json.dumps(data)
	up = urllib.parse.urlparse(url)
	org_headers = {
		"Accept": "*/*",
		"Accept-Encoding": "br, gzip, deflate",
		"Accept-Language": "zh-Hans-CN;q=1",
		"Connection": "keep-alive",
		"Host": up.netloc,
		"User-Agent": "mahua/1.1.8 (iPhone; iOS 12.1.2; Scale/3.00)"
	}
	final_headers = org_headers.copy()
	if headers :
		final_headers.update(headers)

	cookie_jar = RequestsCookieJar()
	if post_type.upper() == 'POST':
		res = requests.post(url,data=str_json,headers=final_headers,cookies=cookie_jar)
	elif post_type.upper() == 'PUT':
		res = requests.put(url,data=str_json,headers=final_headers,cookies=cookie_jar)
	elif post_type.upper() == 'GET':
		res = requests.get(url,headers=final_headers)
	else:
		print('TypeErr')
	res_data = res.text.encode('utf-8').decode('utf-8')
	desc_str = des_descrypt(res_data)
	desc_str = str(desc_str,encoding='utf-8')
	desc_str = ''.join([desc_str.strip().rsplit("}" , 1)[0] ,  "}"] )
	#if res.status_code != requests.codes.ok:	
	return json_dic(desc_str)

def des_descrypt(s):
    secret_key = des_Key
    iv = secret_key
    k = des(secret_key, ECB, iv)
    de = k.decrypt(base64.b64decode(s))
    return de


