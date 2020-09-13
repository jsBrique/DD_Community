# -*- coding: utf-8 -*-
import requests
import time
import wave
import json
import base64
import time
from time import strftime, localtime
import collections
import  os
from request_util import request, authorization
from pydub import AudioSegment
from pydub.playback import play
import redis
old_list = []
old_metalist = []
class Danmu():
	def __init__(self):
		
		self.url = "https://api.live.bilibili.com/ajax/msg"
		self.headers ={
			"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:65.0) Gecko/20100101 Firefox/65.0",
			"Referer": "https://live.bilibili.com/901625?spm_id_from=333.334.b_62696c695f6c697665.13",
			}
		self.data = {
			"roomid":"801580", #replace '_' with roomid #将'_'替换为你想要的抓取弹幕直播间的roomid
			"csrf_token":"",	
			"csrf":"",	
			"visit_id":""
			} 
		self.file=open('../templates/hanhan.txt','a')
		self.init_flag=False
		self.rd= redis.StrictRedis(host='localhost', port=4514, db=0,decode_responses=True)
		self.maxid=self.rd.dbsize()
		#print("<meta http-equiv=\"refresh\" content=\"5\"> <head><title>涵涵哈哈恍恍惚惚哼哼啊啊啊啊</title>   <h1>DD小区</h1>   <h3>建设中...</h3><h5>作者： @砖砖-小鹿砖FPV  <br>涵涵最棒了！！！阿巴阿巴</h5></head>",file=self.file)
	def tts_process(self,text):
		req = request()
		req.init()
		auth = authorization()
		auth.init()

		#request_data = collections.OrderedDict()
		request_data = dict()
		request_data['Action'] = 'TextToStreamAudio'
		request_data['AppId'] = auth.AppId
		request_data['Codec'] = req.Codec
		request_data['Expired'] = int(time.time()) + auth.Expired
		request_data['ModelType'] = req.ModelType
		request_data['PrimaryLanguage'] = req.PrimaryLanguage
		request_data['ProjectId'] = req.ProjectId
		request_data['SampleRate'] = req.SampleRate
		request_data['SecretId'] = auth.SecretId
		request_data['SessionId'] = req.SessionId
		request_data['Speed'] = req.Speed
		request_data['Text'] = text
		request_data['Timestamp'] = int(time.time())
		request_data['VoiceType'] = req.VoiceType
		request_data['Volume'] = req.Volume

		signature = auth.generate_sign(request_data = request_data)
		header = {
			"Content-Type": "application/json",
			"Authorization": signature
		}
		url = "https://tts.cloud.tencent.com/stream"

		r = requests.post(url, headers=header, data=json.dumps(request_data), stream = True)
		i = 1
		filename = 'test.wav'
		wavfile = wave.open(filename, 'wb')
		wavfile.setparams((1, 2, 16000, 0, 'NONE', 'NONE'))
		for chunk in r.iter_content(1000):
			if (i == 1) & (str(chunk).find("Error") != -1) :
				print(chunk)
				return 
			i = i + 1
			wavfile.writeframes(chunk)
			
		wavfile.close()
		try:
			song = AudioSegment.from_wav("test.wav")
			play(song)
		except:
			print("[System] 跳过该条")
		
		
		
	def text_danmu(self,html):
		global old_list, old_metalist
		temp_list = []
		temp_metalist = []
		table=[]
		temp_namelist=[]
		temp_timelist=[]
		# print('===================================================')
		# print( html["data"])
		try:
			for text in html["data"]["room"]:
				temp_list.append(text["text"])
				temp_metalist.append(text["timeline"] +" "+ text["nickname"])
				temp_namelist.append(text["nickname"])
				temp_timelist.append(text["timeline"])
		except:
			temp_list=ord_list
			temp_metalist=old_metalist
		if temp_list == old_list and temp_metalist == old_metalist:
			self.init_flag=True
		else:
			for text_number in range (1,11):
				if "".join(temp_list[:text_number]) in "".join(old_list) and "".join(temp_metalist[:text_number]) in "".join(old_metalist):
					pass
				else:
					try:
						if self.init_flag==True:
							if '涵涵_Live2Dモデリング' in text["nickname"]:
								print(temp_metalist[text_number-1] + " : " +'<br>'+ temp_list[text_number-1],file=self.file)
								self.file.flush()
							print(temp_metalist[text_number-1] + " : " + temp_list[text_number-1])
							self.rd.hset(str(self.maxid)+'T'+temp_timelist[text_number-1],'time',temp_timelist[text_number-1])
							self.rd.hset(str(self.maxid)+'T'+temp_timelist[text_number-1],'name',temp_namelist[text_number-1])
							self.rd.hset(str(self.maxid)+'T'+temp_timelist[text_number-1],'text',temp_list[text_number-1])
							self.maxid+=1
							
						else:
							print('初始化中')
					except:
						pass
					else:
						pass
						#self.tts_process(temp_list[text_number-1])
			old_list = temp_list[:]
			old_metalist = temp_metalist[:]
			# self.file.close()
			
	def get_danmu(self):
		try:
			html = requests.post(url=self.url,headers=self.headers,data=self.data)
			html.json()
			#print(html.text)
			self.text_danmu(eval(html.text))
		except:
			print("弹幕API故障!")

danmuji = Danmu()
count=0
while True:
	danmuji.get_danmu()
	time.sleep(2)
	if count>450:
		os.system("redis-cli -p 4514 bgsave")
		print(strftime("savetime: %Y-%m-%d %H:%M:%S", localtime()))
		count=0
	count+=1
	

	#每1秒钟调用一个刷新弹幕