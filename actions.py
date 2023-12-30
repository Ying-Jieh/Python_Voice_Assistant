from __future__ import print_function
import datetime
from neuralintents import GenericAssistant
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import speech_recognition as sr
import pyttsx3 as tts
import sys
import pafy
import vlc
import time
from datetime import datetime
from playsound import playsound
import pyjokes
import urllib.request
import json
import subprocess
from gtts import gTTS
import tempfile
from pygame import mixer

from youtube_search import get_youtube_urls
from youtube_search import get_youtube_playlist
from youtube_search import get_youtube_playlist_items
from youtube_search import get_youtube_audio_url


def speak(text, filename=None):
		with tempfile.NamedTemporaryFile(delete=True) as temp:
				tts = gTTS(text, lang='zh-TW',slow=False)
				if filename is None:
						filename = "{}.mp3".format(temp.name)
				tts.save(filename)
				mixer.init()
				mixer.music.load(filename)
				mixer.music.play()
				while mixer.music.get_busy() == True:
						continue
				mixer.quit()

def get_audio(limit_time):
	r = sr.Recognizer()
	#r.energy_threshold = 300
	with sr.Microphone() as source:
		#r.adjust_for_ambient_noise(source, duration=0.2)
		r.adjust_for_ambient_noise(source)
		audio = r.listen(source, phrase_time_limit=limit_time)
		said = ""
		try:
				said = r.recognize_google(audio, language='zh-TW')
				print("您所說的話: " + said)
		except sr.UnknownValueError:
				r = sr.Recognizer()
	return said.lower()

def greet():
		hr = int(datetime.now().hour)
		if hr >= 12 and hr < 18:
				hr -= 12
				speak("英杰，下午好")
		elif hr >= 18 and hr < 24:
				speak("英杰，晚上好")
		else:
				speak("英杰，早上好")


def record(text):
		get_audio(10)


def joke():
		joke = pyjokes.get_joke()
		print(joke)
		speak(joke)


def get_time():
		time = datetime.now().strftime('%H:%M')
		hr = int(time.split(":")[0])
		mins = int(time.split(":")[1])
		print("現在時間: " + time)
		if mins=="00":
				#mins == "o'clock"
				mins == "整"
		if hr >= 12:
				hr -= 12
				#speak("It's " + str(hr) + str(mins) + "pm")
				speak(f"現在是下午{str(hr)}點{str(mins)}分")
		else:
				#speak("It's " + str(hr) + str(mins) + "am")
				speak(f"現在是上午{str(hr)}點{str(mins)}分")


weather_dic = {"台北":101340101, "桃園":101340102}
def get_weather(): # 台北編碼101340101  桃園編碼101340102
		url = 'http://www.weather.com.cn/data/cityinfo/101340101.html' 
		obj = urllib.request.urlopen(url) 
		data_b = obj.read() 
		data_s = data_b.decode('utf-8') 
		data_dict = json.loads(data_s) 
		rt = data_dict['weatherinfo'] 
		weather = '台北的溫度是 {} 到 {}，天氣 {} ,' 
		weather = weather.format(rt['temp1'], rt['temp2'], rt['weather']) 
		if '雨' in weather: weather += '今天出門別忘記帶雨傘！' 
		speak(weather)

todo_list = []
def add_todo():
		speak("請問要增加甚麼代辦事項")
		item = get_audio(None)
		todo_list.append(item)
		done = True
		speak(f"我已將, {item}, 加入代辦事項中!")

def show_todos():
		speak("以下是您的代辦事項")
		for item in todo_list:
				speak(item)

def countdown(text):
	if "數" in text:
		idx1 = text.find("時")
	
	if "時" in text:
		idx1 = text.find("時")

	if "分" in text:
		idx2 = text.find("分")
		mins = int(text[idx1+1:idx2])
	else:
		mins = 0

	if "秒" in text:
		idx3 = text.find("秒")
		if "分" in text:
			secs = int(text[idx2+1:idx3])
		else:
			secs = int(text[idx1+1:idx3])

	else:
		secs = 0

	if "分" in text:
		speak(f"倒數計時{mins}分{secs}秒")
	else:
		speak(f"倒數計時{secs}秒")
	total_sec = mins*60 + secs

	if total_sec >= 20:
		for i in range(0,total_sec):
			time.sleep(1)
			if i == 11:
				speak("還剩10秒")
	else:
		for i in range(0, total_sec):
			time.sleep(1)
	speak("時間到")


def youtube_play(text):
	if "清單" not in text and "歌單" not in text:
		if "播放" in text:
			idx1 = text.find("播放")
			track = text[idx1+2:]
		elif "聽" in text:
			idx1 = text.find("聽")
			track = text[idx1+1:]

		track = track.strip()
		speak(f"位您播放{track}")
		print(track)
		urls = get_youtube_urls(track)
		print(urls)

	else:
		playlists = get_youtube_playlist()
		print(playlists)
		speak("請問要播放哪一個歌單")
		text = get_audio(3)
		while True:
			if text in playlists:
				speak(f"位您播放{text}")
				urls, list_item_titles = get_youtube_playlist_items(text)
				print(list_item_titles)
				break
			else:
				speak("我不太明白，請再說一次")
				text = get_audio(3)

	urls, list_item_titles = get_youtube_playlist_items(text)
	#------------------------VLC------------------------#
	media_player = vlc.MediaListPlayer() # creating a media player object
	media_list = vlc.MediaList() # creating a media list object
	instance = vlc.Instance() # creating Instance class object

#	media_index = []
#	media_adr = []

	for url in urls:
		media = instance.media_new(get_youtube_audio_url(url)) # creating a new media
#		media_index.append(media)
		media_list.add_media(media) # adding media to media list

#	print(media_index)

#		index = media_list.index_of_item(media) # getting index of media in media list
#		media_index.append(index)
#		adr = media_list.item_at_index(index) # getting media at the index n in media list
#		media_adr.append(adr)

#	for url in urls:
#		media = get_youtube_audio_url(url)
#		media_list.add_media(media)

	media_player.set_media_list(media_list) # setting media list to the media player
	v = 90
	media_player.get_media_player().audio_set_volume(v)

	n = 0
	media_player.play_item_at_index(n)
	print(f'song number: {n}/{len(urls)-1} : {list_item_titles[n]}')
	print(f'Volume : {v}')

	WAKE = '小杜'
	while True:
		media_player.get_state()
		text = get_audio(3)
		if text.count(WAKE) > 0:
			media_player.set_pause(1)
			playsound("audio/dong.wav")
			text = get_audio(3)
			if '暫' in text:
				media_player.set_pause(1)
				continue
			elif '繼續' in text:
				media_player.set_pause(0)
				continue
			elif '下' in text:
				speak("播放下一首")
				if n==len(urls)-1:
					n=0
				else:
					n += 1
					media_player.play_item_at_index(n)
			elif '上' in text or '前' in text:
				speak("播放上一首")
				if n==0:
						n=len(urls)-1
				else:
						n -= 1
				media_player.play_item_at_index(n)
			elif '停' in text and '暫' not in text or '退' in text:
				media_player.stop()
				speak("退出音樂模式")
				break
			elif '大' in text:
				v += 20
				media_player.get_media_player().audio_set_volume(v)
				print(f'Volume : {v}')
				media_player.set_pause(0)
				continue
			elif '小' in text:
				v -= 20
				media_player.get_media_player().audio_set_volume(v)
				print(f'Volume : {v}')
				media_player.set_pause(0)
				continue
			else:
				speak("抱歉，我不太明白")
				media_player.set_pause(0)
				continue
			print(f'song number: {n}/{len(urls)-1} : {list_item_titles[n]}')