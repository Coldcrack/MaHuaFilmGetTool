#coding=utf-8
__author__ = 'zxlee'
__github__ = 'https://github.com/SmileZXLee/MaHuaFilmGetTool'
import json
import time
import HttpReq
import sys
import os
import platform
from dateutil.parser import parse

#是否是Windows
os_is_windows = platform.system() == 'Windows'
#Host
host = 'http://app.f3v8m6.com'
#程序入口
def main():
	print(u'欢迎使用MaHuaFilmGetTool!')
	while (True):
		search_content = get_search()['search_content']
		if search_content.upper() == 'Q':
			break
		print(u'正在获取搜索结果列表...')
		res = HttpReq.send_req(host +'/search.php?app=com.chengdu.mahuayingshi&q='+search_content,'','','GET')
		if 'data' in res:
			datas = res['data']
			print(u'共%d条结果'%len(datas))
			handle_search_data(datas)
			print('查询完毕！')

		else:
			print(res)


#根据系统获取raw_input中文编码结果
def gbk_encode(str):
	if os_is_windows:
		return str.decode('utf-8').encode('gbk')
	else:
		return str

#获取用户输入搜索条件
def get_search():
	search_content = input('请输入搜索关键字(输入Q退出): ')
	return {'search_content':search_content}

#处理搜索结果列表
def handle_search_data(search_data):
	index = 0
	for sub_data in search_data:
			res = HttpReq.send_req(host +'/detail.php?app=com.chengdu.mahuayingshi&deviceid=85D6TD05-91AD-400E-AC74-BC5083A08AAA&devicetype=0&mp=1&re=1&v=1.1.8&id='+sub_data['id'],'','','GET')
			index = index+1
			print(str(index)+ '.['+ res['data']['title'] + ']')
			res = res['data']
			if 'submovies' in res:
				res = res['submovies']
			for resSub in res.values():
				if type(resSub).__name__ == 'list':

					for per_sub in resSub:
						if type(per_sub).__name__ == 'dict':
							submovies = per_sub['submovies']
						else:
							submovies = per_sub
						for per_ssub in submovies:
							print('[%s]'%per_ssub['title'] + per_ssub['m3u8'])

main()

