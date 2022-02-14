import requests
import os
import json
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

def getCredentials():
    credentials = None

    if os.path.exists("token.pickle"):
        with open("token.pickle", "rb") as token:
            credentials = pickle.load(token)

    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "client_secrets.json", scopes=[
                    "https://www.googleapis.com/auth/youtube.readonly", 
                    "https://www.googleapis.com/auth/youtube", 
                    "https://www.googleapis.com/auth/youtube.force-ssl", 
                    "https://www.googleapis.com/auth/youtubepartner",
                    "https://www.googleapis.com/auth/youtubepartner-channel-audit",
                    "https://www.googleapis.com/auth/youtube.upload", 
                    "https://www.googleapis.com/auth/youtube.channel-memberships.creator",
                    "https://www.googleapis.com/auth/youtube.third-party-link.creator",
                    "https://www.googleapis.com/auth/youtube.download"
                ]
            )

            flow.run_local_server(
                port=8080,
                prompt='consent',
                authorization_prompt_message=''
            )

            credentials = flow.credentials
        with open("token.pickle", "wb") as token:
            pickle.dump(credentials, token)
        #print(credentials.to_json())
    return credentials

def updateVideoTags(videoId):
    with build('youtube', 'v3', static_discovery=False, credentials=getCredentials()) as service:
        try:
            request = service.videos().list(part='snippet', id=videoId)
            response = request.execute()
            videoTitle=response['items'][0]['snippet']['title']
            videoCategoryId=response['items'][0]['snippet']['categoryId']

            #Update Tag of a video
            request = service.videos().update(
                part="snippet",
                body={
                    "id": videoId,
                    "snippet": {
                        "categoryId": videoCategoryId,
                        "tags": [
                            "Srimad Bhagavatam",
                            "Srila Prabhupada",
                            "Krishna premi",
                            "BLISS",
                            "Bhaktivedanta",
                            "Mythili Rajaraman",
                            "Dictations",
                            "Recordings",
                            "audible",
                            "audio book"
                        ],
                        "title": videoTitle
                    }
                }
            )
            response = request.execute()
            with open("response.json", "wt", encoding="UTF-8") as file:
                file.write(json.dumps(response, indent=2))
        except requests.HTTPError as e:
            print('Error response status code : {0}, reason : {1}'.format(e.status_code, e.error_details))

def channelSummary(channelId="UCLbwWE1OTFQyfXT7O3u6pbw"):
    with build('youtube', 'v3', static_discovery=False, credentials=getCredentials()) as service:
        try:
            ##Channel Summary
            request = service.channels().list(part='statistics', id=channelId)
            response = request.execute()
            print("Channel Summary of channelId = " + channelId + " is:")
            print(json.dumps(response['items'][0]['statistics'], indent=2))
        except requests.HTTPError as e:
            print('Error response status code : {0}, reason : {1}'.format(e.status_code, e.error_details))

def listPlaylist(channelId="UCLbwWE1OTFQyfXT7O3u6pbw"):
    with build('youtube', 'v3', static_discovery=False, credentials=getCredentials()) as service:
        try:
            ##Channel Summary
            hasNextPage=True
            firstPage=True
            playlists=[]
            while hasNextPage:
                if firstPage:
                    request = service.playlists().list(part='snippet,contentDetails', channelId=channelId, maxResults=25)
                    firstPage=False
                else:
                    request = service.playlists().list_next(request,response)
                response = request.execute()
                for item in response['items']:
                    playlists.append({
                        'playlistId': item['id'],
                        'title': item['snippet']['title'],
                        'videoCount': item['contentDetails']['itemCount']
                    })
                    print(item['id'],item['snippet']['title'],item['contentDetails']['itemCount'])
                if 'nextPageToken' in response:
                    hasNextPage = True
                else:
                    hasNextPage = False
            with open("youtube_playlists.json", "wt", encoding="UTF-8") as file:
                file.write(json.dumps(playlists, indent=2))
        except requests.HTTPError as e:
            print('Error response status code : {0}, reason : {1}'.format(e.status_code, e.error_details))

def listPlaylistItems(playlistId="PLdBTiOEoG70mV-0PAAG5NFWiXGFZy1inB"):
    with build('youtube', 'v3', static_discovery=False, credentials=getCredentials()) as service:
        try:
            ##Channel Summary
            hasNextPage=True
            firstPage=True
            videoList=[]
            with open("response.json", "wt", encoding="UTF-8") as file:
                file.write('[\n')
                while hasNextPage:
                    if firstPage:
                        request = service.playlistItems().list(part='snippet,contentDetails', playlistId=playlistId, maxResults=25)
                        firstPage=False
                    else:
                        request = service.playlistItems().list_next(request,response)
                    response = request.execute()

                    for item in response['items']:
                        videoList.append({
                            'title': item['snippet']['title'],
                            'description': item['snippet']['description'],
                            'publishedAt': item['snippet']['publishedAt'],
                            'position': item['snippet']['position'],
                            'videoId': item['snippet']['resourceId']['videoId']
                        })

                    if 'nextPageToken' in response:
                        hasNextPage = True
                    else:
                        hasNextPage = False
                        file.write(']\n')

                    if not firstPage:
                        file.write(',\n')
                    file.write(json.dumps(response, indent=2))

            with open("videosInPlayList-"+playlistId+".json", "wt", encoding="UTF-8") as file:
                file.write(json.dumps(videoList, indent=2))
        except requests.HTTPError as e:
            print('Error response status code : {0}, reason : {1}'.format(e.status_code, e.error_details))
