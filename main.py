from playsound import playsound
from actions import speak
from actions import get_audio
from actions import greet
from actions import youtube_play
from actions import get_time
from actions import record
from actions import get_weather
from actions import add_todo
from actions import show_todos
todo_list = []
from actions import countdown
from actions import joke

import concurrent.futures

def detection():
    print("Listening...")
    text = get_audio(3)
    if text.count(WAKE) > 0:
        playsound("audio/dong.wav")
        text = get_audio(3)

    return text

WAKE = "小杜"
playsound("audio/sound.wav")
greet()

while True:

    text = detection()
    if "播放" in text or "聽" in text:
        youtube_play(text)
        #f2 = executor.submit(youtube_play, text)               

    if "幾點" in text or "時間" in text:
        get_time()

    if "錄音" in text or "留言" in text:
        record()

    if "笑話" in text:
        joke()

    if "天氣" in text or "下雨" in text:
        get_weather()

    if "增" in text and "待辦" in text:
        add_todo()

    if "什麼" in text and "待辦" in text:
        show_todos()

    if "數" in text or "計時" in text:
        countdown(text)

'''
        NOTE_STRS = ["筆記", "寫下", "記下"]
        for phrase in NOTE_STRS:
            if phrase in text:
                speak("您想要我寫下甚麼")
                note_text = get_audio(None)
                note(note_text)
                speak("我已幫你寫下")


        ALARM_STRS = ["叫我", "鬧鐘"]
        for phrase in ALARM_STRS:
            if phrase in text:
                pass
'''