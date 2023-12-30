import pafy
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import vlc
import time
import os
import pickle


def get_youtube_urls(text):
    api_key = 'AIzaSyCDgIKkD9JcwbCNl12uQEHRq1dpBE28hYk'

    vids = [] # 存 videoId
    urls = [] # 存 完整網址

    ### 搜尋 youtube 並取得 videoId ###
    with build('youtube', 'v3', developerKey=api_key) as youtube:
        req = text
        request = youtube.search().list(
                part = 'snippet',
                type = 'video', #用 relatedToVideoId 就要設 type='video'
                #relatedToVideoId = first_vid, #找跟這個id相關的影片 (找到的網址會怪怪的)
                order = 'relevance', # 依關聯性搜尋
                maxResults = 1
        )

    response = request.execute()
    #print(response)


    for item in response['items']:
        vids.append(item['id']['videoId'])

    #print(vids) # 搜尋結果

    for vid in vids:
        url = f"https://www.youtube.com/watch?v={vid}"
        urls.append(url)

    #print(urls)

    return urls


def get_youtube_playlist():
    credentials = None

    titles = []

    #token.pickle stores the user's credentials from previously successful logins
    if os.path.exists("token.pickle"):
        print("Loading Credentials From File...")
        with open("token.pickle", "rb") as token:
            credentials = pickle.load(token)

    # If there are no valid credentials available, then either refresh the token or log in.
    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            print('Refreshing Access Token...')
            credentials.refresh(Request())
        else:
            print('Fetching New Tokens...')
            flow = InstalledAppFlow.from_client_secrets_file(
                'client_secrets.json',
                scopes=['https://www.googleapis.com/auth/youtube.readonly'] 
            )

            flow.run_local_server(port=8080, prompt='consent', authorization_prompt_message='')
            credentials = flow.credentials

            #save the credentials for the next run
            with open("token.pickle", "wb") as f:
                print("Saving Credentials for Future Use...")
                pickle.dump(credentials, f)


    with build('youtube', 'v3', credentials=credentials) as youtube:
        request = youtube.playlists().list(
            part="snippet,contentDetails",
            maxResults=6,
            mine=True #only return playlists owned by the authenticated user.
        )

    response = request.execute()
    #print(response)

    for item in response["items"]:
        title = item["snippet"]["localized"]["title"]
        titles.append(title)

    for i in range(len(titles)):
        titles[i] = titles[i].lower()

    #print(titles) #['我的歌單', 'LoFi', 'Youtube API', 'Jarvis', 'Favorites']

    return titles


def get_youtube_playlist_items(text):
    credentials = None

    list_titles = []
    list_item_titles = []
    lids = []
    vids = []
    urls = []
    dic = {}

    #token.pickle stores the user's credentials from previously successful logins
    if os.path.exists("token.pickle"):
        print("Loading Credentials From File...")
        with open("token.pickle", "rb") as token:
            credentials = pickle.load(token)

    # If there are no valid credentials available, then either refresh the token or log in.
    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            print('Refreshing Access Token...')
            credentials.refresh(Request())
        else:
            print('Fetching New Tokens...')
            flow = InstalledAppFlow.from_client_secrets_file(
                'client_secrets.json',
                scopes=['https://www.googleapis.com/auth/youtube.readonly'] 
            )

            flow.run_local_server(port=8080, prompt='consent', authorization_prompt_message='')
            credentials = flow.credentials

            #save the credentials for the next run
            with open("token.pickle", "wb") as f:
                print("Saving Credentials for Future Use...")
                pickle.dump(credentials, f)


    with build('youtube', 'v3', credentials=credentials) as youtube:
        request = youtube.playlists().list(
            part="snippet,contentDetails",
            maxResults=6,
            mine=True #only return playlists owned by the authenticated user.
        )

    response = request.execute()
    #print(response)

    for item in response["items"]:
        list_title = item["snippet"]["localized"]["title"]
        lid = item["id"]
        list_titles.append(list_title)
        lids.append(lid)
        dic[list_title] = lid

    #print(titles) #['我的歌單', 'LoFi', 'Youtube API', 'Jarvis', 'Favorites']
    #print(lids) #['PLnP8rXqEznWI60OKM7MgdtJQos6kO26qp', 'PLnP8rXqEznWIVGIKSC1IS14sN7Y5h1ujQ', 'PLnP8rXqEznWL4JwhwyKusXGlfHnX1uxAz', 'PLnP8rXqEznWIcZ8s58afxGwY3Xvsv4sSr', 'FLVbIyN6TMuYFqHt1UZXTXIw']
    #print(dic)
    '''
    {'我的歌單': 'PLnP8rXqEznWI60OKM7MgdtJQos6kO26qp', 
    'LoFi': 'PLnP8rXqEznWIVGIKSC1IS14sN7Y5h1ujQ', 
    'Youtube API': 'PLnP8rXqEznWL4JwhwyKusXGlfHnX1uxAz', 
    'Jarvis': 'PLnP8rXqEznWIcZ8s58afxGwY3Xvsv4sSr', 
    'Favorites': 'FLVbIyN6TMuYFqHt1UZXTXIw'}
    '''

    playlistName = text
    playlistId = dic[playlistName]

    with build('youtube', 'v3', credentials=credentials) as youtube:
        request = youtube.playlistItems().list(
            part="snippet,contentDetails",
            maxResults=6,
            playlistId=playlistId
        )

    response = request.execute()

    #print(response)

    for item in response["items"]:
        vid = item["contentDetails"]["videoId"]
        vids.append(vid)
        url = f"https://www.youtube.com/watch?v={vid}"
        urls.append(url)
        list_item_title = item["snippet"]["title"]
        list_item_titles.append(list_item_title)
        #yt_link = f"https://www.youtube.com/watch?v={vid}&list={dic['我的歌單']}"

    #print(list_item_titles)
    #print(vids)
    #print(urls)

    return urls, list_item_titles

# Function to get streaming links for YouTube URLs
def get_youtube_audio_url(url):
    video = pafy.new(url)
    best_audio = video.getbestaudio()
    audio_url = best_audio.url
    return audio_url

