import http.client
import httplib2
import requests
import random
import os
import re
import time
import json
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import argparse

# api_key="??"

# Explicitly tell the underlying HTTP transport library not to retry, since
# we are handling retry logic ourselves.
httplib2.RETRIES = 1

# Maximum number of times to retry before giving up.
MAX_RETRIES = 10

# Always retry when these exceptions are raised.
RETRIABLE_EXCEPTIONS = (httplib2.HttpLib2Error, IOError, http.client.NotConnected,
                        http.client.IncompleteRead, http.client.ImproperConnectionState,
                        http.client.CannotSendRequest, http.client.CannotSendHeader,
                        http.client.ResponseNotReady, http.client.BadStatusLine)

# Always retry when an apiclient.errors.HttpError with one of these status
# codes is raised.
RETRIABLE_STATUS_CODES = [500, 502, 503, 504]

VALID_PRIVACY_STATUSES = ("unlisted", "public", "private")

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
        # print(credentials.to_json())
    return credentials


def channelSummary(channelId="UCLbwWE1OTFQyfXT7O3u6pbw"):
    with build('youtube', 'v3', static_discovery=False, credentials=getCredentials()) as service:
        try:
            # Channel Summary
            request = service.channels().list(part='statistics', id=channelId)
            response = request.execute()
            print("Channel Summary of channelId = " + channelId + " is:")
            print(json.dumps(response['items'][0]['statistics'], indent=2))
        except requests.HTTPError as e:
            print('Error response status code : {0}, reason : {1}'.format(
                e.status_code, e.error_details))


def listPlaylist(channelId="UCLbwWE1OTFQyfXT7O3u6pbw"):
    with build('youtube', 'v3', static_discovery=False, credentials=getCredentials()) as service:
        try:
            # Channel Summary
            hasNextPage = True
            firstPage = True
            playlists = []
            while hasNextPage:
                if firstPage:
                    request = service.playlists().list(part='snippet,contentDetails',
                                                       channelId=channelId, maxResults=25)
                    firstPage = False
                else:
                    request = service.playlists().list_next(request, response)
                response = request.execute()
                for item in response['items']:
                    playlists.append({
                        'playlistId': item['id'],
                        'title': item['snippet']['title'],
                        'videoCount': item['contentDetails']['itemCount']
                    })
                    print(item['id'], item['snippet']['title'],
                          item['contentDetails']['itemCount'])
                if 'nextPageToken' in response:
                    hasNextPage = True
                else:
                    hasNextPage = False
            with open("youtube_playlists.json", "wt", encoding="UTF-8") as file:
                file.write(json.dumps(playlists, indent=2))
        except requests.HTTPError as e:
            print('Error response status code : {0}, reason : {1}'.format(
                e.status_code, e.error_details))


def listPlaylistItems(playlistId="PLdBTiOEoG70mV-0PAAG5NFWiXGFZy1inB"):
    print("Inside listPlaylistItems. playlistId = %s" % playlistId)
    with build('youtube', 'v3', static_discovery=False, credentials=getCredentials()) as service:
        try:
            # Channel Summary
            hasNextPage = True
            firstPage = True
            videoList = []
            with open("response.json", "wt", encoding="UTF-8") as file:
                file.write('[\n')
                while hasNextPage:
                    if firstPage:
                        request = service.playlistItems().list(part='snippet,contentDetails',
                                                               playlistId=playlistId, maxResults=25)
                        firstPage = False
                    else:
                        request = service.playlistItems().list_next(request, response)
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

            print("writing videosInPlayList-%s.json" % playlistId)
            with open("videosInPlayList-"+playlistId+".json", "wt", encoding="UTF-8") as file:
                file.write(json.dumps(videoList, indent=2))
        except requests.HTTPError as e:
            print('Error response status code : {0}, reason : {1}'.format(
                e.status_code, e.error_details))

def get_lines(filename):
  file = open(filename, 'r', encoding="UTF-8")
  Lines = file.read().splitlines()
  file.close()
  return Lines

def enrichDuration(playlistId):
    #listPlaylistItems(playlistId=playlistId)
    with open("videosInPlayList-"+playlistId+".json", "r", encoding="UTF-8") as f:
        playlist = json.load(f)

    for video in playlist:
        if not ('duration' in video):
            response = readVideoDetails(video['videoId'])
            duration = response['items'][0]['contentDetails']['duration']
            video['duration'] = duration
            time.sleep(1)
        print(video['videoId'] + "|" + video['duration'].replace("PT","00:").replace("M",":").replace("S","") + "|" + video['title'])

    with open("videosInPlayList-"+playlistId+"-new.json", "wt", encoding="UTF-8") as file:
        file.write(json.dumps(playlist, indent=2))

def updateRSVideoTags(videoId=None, videoNumber=None, categoryId=10, playlistId="PLdBTiOEoG70n_aTSZgIGi3pOtyO7D2Tky", fromItem=None, toItem=None):
    USERPROFILE=os.environ['USERPROFILE']
    RSFOLDER=USERPROFILE + "\\books\\srisrianna\\radhikashathakam\\"
    index_file=RSFOLDER + "index.txt"
    index_lines=get_lines(index_file)
    song_number=1
    with build('youtube', 'v3', static_discovery=False, credentials=getCredentials()) as service:
        playlist = []
        try:
            if videoId != None and videoNumber != None:
                playlist.append({'videoId': videoId})
                song_number=videoNumber
            else:
                listPlaylistItems(playlistId=playlistId)
                with open("videosInPlayList-"+playlistId+".json", "r", encoding="UTF-8") as f:
                    playlist = json.load(f)

            response_file = open("response_"+time.strftime("%Y%m%d%H%M%S",
                                 time.localtime())+".log", "wt", encoding="UTF-8")
            response_file.write("[\n")
            playlistItem=0
            for video in playlist:
                if (fromItem == None or (fromItem != None and playlistItem+1 > fromItem)) and (toItem == None or (toItem != None and playlistItem+1 < toItem)):
                    title_meta=index_lines[song_number].rstrip("\n").split("|")
                    raga_meta=title_meta[1].split(" - ")
                    if video['videoId'] != None:
                        videoCategoryId = categoryId
                        videoTitle = "Radhika Shatakam " + str(song_number).zfill(3) + " | " + title_meta[0].rstrip(" ") + " | " + raga_meta[0].lstrip(" ")
                        videoDescription = """
#RadhikaShatakam #SriSriAnna #MythiliRajaraman

Song %d: %s
Ragam: %s
Talam: %s
Composed by: Sri Sri Krishnapremi Swamigal

Part of this playlist: https://www.youtube.com/playlist?list=PLdBTiOEoG70n_aTSZgIGi3pOtyO7D2Tky
""" % (song_number,title_meta[0],raga_meta[0],raga_meta[1])

                        # Update Tag of a video
                        request = service.videos().update(
                            part="snippet",
                            body={
                                "id": video['videoId'],
                                "snippet": {
                                    "categoryId": videoCategoryId,
                                    "tags": [
                                        "Radhika Shatakam",
                                        "Songs on Radha",
                                        "Radha Story",
                                        "Radhika Shathakam",
                                        "Radhika Sathakam",
                                        "Radhika Satakam",
                                        "Raas Leela",
                                        "Krishna",
                                        "premi",
                                        "anna",
                                        "bhajan",
                                        "lyrics",
                                        "sanskrit",
                                        "krishnapremi",
                                        "song " + str(song_number).zfill(3),
                                        title_meta[0].rstrip(" "),
                                        raga_meta[0].lstrip(" ")
                                    ],
                                    "title": videoTitle,
                                    "description": videoDescription
                                }
                            }
                        )
                        response = request.execute()
                        response_file.write(json.dumps(response, indent=2))
                        response_file.write(",\n")
                        time.sleep(5) #delay 1 second to catchup
                song_number+=1
                playlistItem+=1
            response_file.write("]\n")
            response_file.close()
        except requests.HTTPError as e:
            print('Error response status code : {0}, reason : {1}'.format(
                e.status_code, e.error_details))

def readVideoDetails(videoId):
    response=None
    with build('youtube', 'v3', static_discovery=False, credentials=getCredentials()) as service:
        request = service.videos().list(
            part='contentDetails', id=videoId)
        response = request.execute()
    return response

def get_title(canto=0,chapter=0):
    titles = [[
                "1.01 - Questions by the Sages",
                "1.02 - Divinity and Divine Service",
                "1.03 - Krishna Is the Source of All Incarnations",
                "1.04 - The Appearance of Sri Narada",
                "1.05 - Narada's Instructions on Srimad-Bhagavatam for Vyasadeva",
                "1.05 - Narada's Instructions on Srimad-Bhagavatam for Vyasadeva",
                "1.06 - Conversation Between Narada and Vyasadeva",
                "1.07 - The Son of Drona Punished",
                "1.08 - Prayers by Queen Kunti and Parikshit Saved",
                "1.09 - The Passing Away of Bhishmadeva in the Presence of Krishna",
                "1.10 - Departure of Lord Krishna for Dvaraka",
                "1.11 - Lord Krishna's Entrance into Dvaraka",
                "1.12 - Birth of Emperor Parikshit",
                "1.13 - Dhrtarashtra Quits Home",
                "1.14 - The Disappearance of Lord Krishna",
                "1.15 - The Pandavas Retire Timely",
                "1.16 - How Parikshit Received the Age of Kali",
                "1.17 - Punishment and Reward of Kali",
                "1.18 - Maharaja Parikshit Cursed by a Brahmana Boy",
                "1.19 - The Appearance of Sri Suka"
              ], [
                "2.01 - The First Step in God Realization",
                "2.02 - The Lord in the Heart",
                "2.03 - Pure Devotional Service - The Change in Heart",
                "2.04 - The Process of Creation",
                "2.05 - The Cause of All Causes",
                "2.06 - Purusha-sukta Confirmed",
                "2.07 - Scheduled Incarnations with Specific Functions",
                "2.08 - Questions by King Parikshit",
                "2.09 - Answers by Citing the Lord's Verishion",
                "2.10 - Bhagavatam Is the Answer to All Questions",
              ], [
                "3.01 - Questions by Vidura",
                "3.02 - Remembrance of Lord Krishna",
                "3.03 - The Lord's Pastimes Out of Vrndavana",
                "3.04 - Vidura Approaches Maitreya",
                "3.05 - Vidura's Talks with Maitreya",
                "3.06 - Creation of the Universal Form",
                "3.07 - Further Inquires by Vidura",
                "3.08 - Manifestation of Brahma from Garbhodakasayi Visnu",
                "3.09 - Brahma's Prayers for Creative Energy",
                "3.10 - Divisions of the Creation",
                "3.11 - Calculation of Time, from the Atom",
                "3.12 - Creation of the Kumaras and Others",
                "3.13 - The Appearance of Lord Varaha",
                "3.14 - Pregnancy of Diti in the Evening",
                "3.15 - Description of the Kingdom of God",
                "3.16 - Jaya and Vijaya Cursed by the Sages",
                "3.17 - Victory of Hiranyaksa Over the Universes",
                "3.18 - The Battle Between Varahamurthi and Hiranyaksa",
                "3.19 - The Killing of the Demon Hiranyaksa",
                "3.20 - Conversation Between Maitreya and Vidura",
                "3.21 - Conversation Between Manu and Kardama",
                "3.22 - The Marriage of Kardama Muni and Devahuti",
                "3.23 - Devahuti's Lamentation",
                "3.24 - The Renunciation of Kardama Muni",
                "3.25 - The Glories of Devotional Service",
                "3.26 - Fundamental Principles of Material Nature",
                "3.27 - Understanding Material Nature",
                "3.28 - Kapila's Instructions for Devotional Service",
                "3.29 - Explanation of Devotional Service by Lord Kapila",
                "3.30 - Description by Lord Kapila of Adverse Fruitive Activities",
                "3.31 - Lord Kapila's Instructions on the Movements of the Living",
                "3.32 - Entanglement in Fruitive Activities",
                "3.33 - Activities of Kapila",
              ], [
                "4.01 - Genealogical Table of the Daughters of Manu",
                "4.02 - Daksa Curses Lord Siva",
                "4.03 - Talks Between Lord Siva and Sati",
                "4.04 - Sati Quits Her Body",
                "4.05 - Frustration of the Sacrifice of Daksa",
                "4.06 - Brahma Satisfies Lord Siva",
                "4.07 - The Sacrifice Performed by Daksa",
                "4.08 - Dhruva Maharaja Leaves Home for the Forest",
                "4.09 - Dhruva Maharaja Returns Home",
                "4.10 - Dhruva Maharaja's Fight With the Yaksas",
                "4.11 - Svayambhuva Manu Advises Dhruva Maharaja to Stop Fighting",
                "4.12 - Dhruva Maharaja Goes Back to Godhead",
                "4.13 - Description of the Descendants of Dhruva Maharaja",
                "4.14 - The Story of King Vena",
                "4.15 - King Prthu's Appearance and Coronation",
                "4.16 - Praise of King Prthu by the Professional Reciters",
                "4.17 - Maharaja Prthu Becomes Angry at the Earth",
                "4.18 - Prthu Maharaja Milks the Earth Planet",
                "4.19 - King Prthu's One Hundred Horse Sacrifices",
                "4.20 - Lord Visnu's Appearance in front of Maharaja Prthu",
                "4.21 - Instructions by Maharaja Prthu",
                "4.22 - Prthu Maharaja's Meeting with the Four Kumaras",
                "4.23 - Maharaja Prthu's Going Back Home",
                "4.24 - Chanting the Song Sung by Lord Siva",
                "4.25 - The Descriptions of the Characteristics of King Puranjana",
                "4.26 - King Puranjana Goes for hunting and His Queen Becomes Angry",
                "4.27 - Attack by Candavega on the City of King Puranjana",
                "4.28 - Puranjana Becomes a Woman in the Next Life",
                "4.29 - Talks Between Narada and King Pracinabarhi",
                "4.30 - The Activities of the Pracetas",
                "4.31 - Narada Instructs the Pracetas",
              ], [
                "5.01 - The Activities of Maharaja Priyavrata",
                "5.02 - The Activities of Maharaja Agnidhra",
                "5.03 - Risabhadeva Appearance in the Womb of Merudevi, King Nabhi",
                "5.04 - The Characteristics of Rsabhadeva, the Supreme Lord",
                "5.05 - Lord Rsabhadeva's Teachings to His Sons",
                "5.06 - The Activities of Lord Rsabhadeva",
                "5.07 - The Activities of King Bharata",
                "5.08 - A Description of the Character of Bharata Maharaja",
                "5.09 - The Supreme Character of Jada Bharata",
                "5.10 - The Discussion Between Jada Bharata and Maharaja Rahugana",
                "5.11 - Jada Bharata Instructs King Rahugana",
                "5.12 - Conversation Between Maharaja Rahugana and Jada Bharata",
                "5.13 - Further Talks Between King Rahugana and Jada Bharata",
                "5.14 - The Material World as the Great Forest of Enjoyment",
                "5.15 - The Glories of the Descendants of King Priyavrata",
                "5.16 - A Description of Jambudvipa",
                "5.17 - The Descent of the River Ganges",
                "5.18 - The Prayers Offered by the Residents of Jambudvipa",
                "5.19 - A Description of the Island of Jambudvipa",
                "5.20 - Studying the Structure of the Universe",
                "5.21 - The Movements of the Sun",
                "5.22 - The Orbits of the Planets",
                "5.23 - The Sisumara Planetary Systems",
                "5.24 - The Subterranean Heavenly Planets",
                "5.25 - The Glories of Lord Ananta",
                "5.26 - A Description of the Hellish Planets",
              ], [
                "6.01 - The History of the Life of Ajamila",
                "6.02 - Ajamila Delivered by the Visnudutas",
                "6.03 - Yamaraja Instructs His Messengers",
                "6.04 - The Hamsa-guhya Prayers",
                "6.05 - Narada Muni Cursed by Prajapati Daksa",
                "6.06 - The Progeny of the Daughters of Daksa",
                "6.07 - Indra Offends His Spiritual Master, Brhaspati",
                "6.08 - The Narayana-kavaca Shield",
                "6.09 - Appearance of the Demon Vrtrasura",
                "6.10 - The Battle Between the Demigods and Vrtrasura",
                "6.11 - The Transcendental Qualities of Vrtrasura",
                "6.12 - Vrtrasura's Glorious Death",
                "6.13 - King Indra Afflicted by Sinful Reaction",
                "6.14 - King Citraketu's Lamentation",
                "6.15 - The Saints Narada and Angira Instruct King Citraketu",
                "6.16 - King Citraketu Meets the Supreme Lord",
                "6.17 - Mother Parvati Curses Citraketu",
                "6.18 - Diti Vows to Kill King Indra",
                "6.19 - Performing the Pumsavana Ritualistic Ceremony",
              ], [
                "7.01 - The Supreme Lord Is Equal to Everyone",
                "7.02 - Hiranyakasipu, King of the Demons",
                "7.03 - Hiranyakasipu's Plan to Become Immortal",
                "7.04 - Hiranyakasipu Terrorizes the Universe",
                "7.05 - Prahlada Maharaja, the Saintly Son of Hiranyakasipu",
                "7.06 - Prahlada Instructs His Demoniac Schoolmates",
                "7.07 - What Prahlada Learned in the Womb",
                "7.08 - Lord Nrishimhadeva Slays the King of the Demons",
                "7.09 - Prahlada Pacifies Lord Nrishimhadeva with Prayers",
                "7.10 - Prahlada, the Best Among Exalted Devotees",
                "7.11 - The Perfect Society_ Four Social Classes",
                "7.12 - The Perfect Society_ Four Spiritual Classes",
                "7.13 - The Behavior of a Perfect Person",
                "7.14 - Ideal Family Life",
                "7.15 - Instructions for Civilized Human Beings",
              ], [
                "8.01 - The Manus, Administrators of the Universe",
                "8.02 - The Elephant Gajendra's Crisis",
                "8.03 - Gajendra's Prayers of Surrender",
                "8.04 - Gajendra Returns to the Spiritual World",
                "8.05 - The Demigods Appeal to the Lord for Protection",
                "8.06 - The Demigods and Demons Declare a Truce",
                "8.07 - Lord Siva Saves the Universe by Drinking Poison",
                "8.08 - The Churning of the Milk Ocean",
                "8.09 - The Lord Incarnates as Mohini-Murti",
                "8.10 - The Battle Between the Demigods and the Demons",
                "8.11 - King Indra Annihilates the Demons",
                "8.12 - The Mohini-murti Incarnation Bewilders Lord Siva",
                "8.13 - Description of Future Manus",
                "8.14 - The System of Universal Management",
                "8.15 - Bali Maharaja Conquers the Heavenly Planets",
                "8.16 - Executing the Payo-vrata Process of Worship",
                "8.17 - The Supreme Lord Agrees to Become Aditi's Son",
                "8.18 - Lord Vamanadeva, the Dwarf Incarnation",
                "8.19 - Lord Vamanadeva Begs Charity from Bali Maharaja",
                "8.20 - Bali Maharaja Surrenders the Universe",
                "8.21 - Bali Maharaja Arrested by the Lord",
                "8.22 - Bali Maharaja Surrenders His Life",
                "8.23 - The Demigods Regain the Heavenly Planets",
                "8.24 - Matsya, the Lord's Fish Incarnation",
              ], [
                "9.01 - King Sudyumna Becomes a Woman",
                "9.02 - The Dynasties of the Sons of Manu",
                "9.03 - The Marriage of Sukanya and Cyavana Muni",
                "9.04 - Ambarisa Maharaja Offended by Durvasa Muni",
                "9.05 - Durvasa Muni's Life Spared",
                "9.06 - The Downfall of Saubhari Muni",
                "9.07 - The Descendants of King Mandhata",
                "9.08 - The Sons of Sagara Meet Lord Kapiladeva",
                "9.09 - The Dynasty of Amsuman",
                "9.10 - The Pastimes of the Supreme Lord, Ramacandra",
                "9.11 - Lord Ramacandra Rules the World",
                "9.12 - The Dynasty of Kusa, the Son of Lord Ramacandra",
                "9.13 - The Dynasty of Maharaja Nimi",
                "9.14 - King Pururava Enchanted by Urvasi",
                "9.15 - Parasurama, the Lord's Warrior Incarnation",
                "9.16 - Lord Parasurama Destroys the World's Ruling Class",
                "9.17 - The Dynasties of the Sons of Pururava",
                "9.18 - King Yayati Regains His Youth",
                "9.19 - King Yayati Achieves Liberation",
                "9.20 - The Dynasty of Puru",
                "9.21 - The Dynasty of Bharata",
                "9.22 - The Descendants of Ajamidha",
                "9.23 - The Dynasties of the Sons of Yayati",
                "9.24 - Krishna the Supreme Lord",
              ], [
                "10.01 - The Advent Of Lord Krishna",
                "10.02 - Prayers by Gods to the Lord",
                "10.03 - Birth of Lord Krishna",
                "10.04 - Atrocities of Kamsa",
                "10.05 - Meeting of Nanda & Vasudeva",
                "10.06 - Killing of Demon Putana",
                "10.07 - Killing of Demon Trnavarta",
                "10.08 - Lord shows Universal Form",
                "10.09 - Mother Yashoda Binds Lord Krishna",
                "10.10 - Deliverance of Yamala-Arjuna Trees",
                "10.11 - The Childhood Pastimes of Lord Krishna",
                "10.12 - The Killing of Demon Aghasura",
                "10.13 - The Stealing of the Calves & Boys by Brahma",
                "10.14 - Brahma's Prayers to Lord Krishna",
                "10.15 - The Killing of Demon Dhenuka",
                "10.16 - Sri Krishna Chastises Serpent Kaliya",
                "10.17 - The History of Kaliya",
                "10.18 - Lord Balarama Kills Demon Pralamba",
                "10.19 - Lord Swallows Forest Fire",
                "10.20 - The Rainy & Autumn Seasons in Vrndavana",
                "10.21 - The Gopis Glorify the Song of Krishna's Flute",
                "10.22 - Lord Krishna Steals the Garments of the Gopis",
                "10.23 - The Brahmanas' Wives Blessed",
                "10.24 - Worshiping Govardhana Hill",
                "10.25 - Lord Krishna Lifts Govardhana Hill",
                "10.26 - The Wonderful Krishna",
                "10.27 - Lord Indra & Mother Surabhi offer Prayers",
                "10.28 - Lord Krishna Rescues Nanda",
                "10.29 - Krishna and the Gopis meet for Rasa Dance",
                "10.30 - The Gopis Search for Krishna",
                "10.31 - The Gopis Song of Separation",
                "10.32 - The Reunion",
                "10.33 - The Rasa Dance",
                "10.34 - Nanda saved and Sankhachuda Slain",
                "10.35 - The Gopis sing of Krishna as He Wanders in the Forest",
                "10.36 - Slaying of Arishtasura",
                "10.37 - The Killling of Demon Kesi and Vyoma",
                "10.38 - Akrura's arrival in Vrndavana",
                "10.39 - Akrura's Vision",
                "10.40 - The Prayers of Akrura",
                "10.41 - Krishna and Balarama enter Mathura",
                "10.42 - Breaking of the Sacrificial Bow",
                "10.43 - Krishna kills the Elephant Kuvalayapida",
                "10.44 - The Killling of Kamsa",
                "10.45 - Krishna Rescues His Teacher's Son",
                "10.46 - Uddhava Visits Vrndavana",
                "10.47 - The Song of the Bee",
                "10.48 - Krishna Pleases His Devotees",
                "10.49 - Akrura's Mission in Hastinapura",
                "10.50 - Krishna Establishes the City of Dvaraka",
                "10.51 - The Deliverance of Mucukunda",
                "10.52 - Rukmini's Message to Lord Krishna",
                "10.53 - Krishna Kidnaps Rukmini",
                "10.54 - The Marriage of Krishna and Rukmini",
                "10.55 - The History of Pradyumna",
                "10.56 - The Syamantaka Jewel",
                "10.57 - Satrajit Murdered, the Jewel Returned",
                "10.58 - Krishna Marries Five Princess",
                "10.59 - The Killing of the Demon Naraka",
                "10.60 - Lord Krishna Teases Queen Rukmini",
                "10.61 - Lord Balarama Slays Rukmi",
                "10.62 - The Meeting of Usa and Aniruddha",
                "10.63 - Lord Krishna Fights with Banasura",
                "10.64 - The Deliverance of King Nrga",
                "10.65 - Lord Balarama Visits Vrndavana",
                "10.66 - Paundraka, the False Vasudeva",
                "10.67 - Lord Balarama Slays Dvivida Gorilla",
                "10.68 - The Marriage of Samba",
                "10.69 - Narada Muni Visits Lord Krishna's Palaces in Dvaraka",
                "10.70 - Lord Krishna's Daily Activities",
                "10.71 - The Lord Travels to Indraprastha",
                "10.72 - The Slaying of the Demon Jarasandha",
                "10.73 - Lord Krishna Blesses the Liberated Kings",
                "10.74 - The Deliverance of Sisupala at the Rajasuya Sacrifice",
                "10.75 - Duryodhana Humiliated",
                "10.76 - The Battle Between Salva and the Vrsnis",
                "10.77 - Lord Krishna Slays the Demon Salva",
                "10.78 - The Killing of Dantavakra, Viduratha and Romaharsana",
                "10.79 - Lord Balarama Goes on Pilgrimage",
                "10.80 - The Brahmana Sudama Visits Lord Krishna in Dvaraka",
                "10.81 - The Lord Blesses Sudama Brahmana",
                "10.82 - Krishna and Balarama Meet the Inhabitants of Vrndavana",
                "10.83 - Draupadi Meets the Queens of Krishna",
                "10.84 - The Sages' Teachings at Kuruksetra",
                "10.85 - Lord Krishna Instructs Vasudeva and Retrieves Devaki's Sons",
                "10.86 - Arjuna Kidnaps Subhadra, and Krishna Blesses His Devotees",
                "10.87 - The Prayers of the Personified Vedas",
                "10.88 - Lord Siva Saved from Vrkasura",
                "10.89 - Krishna and Arjuna Retrieve a Brahmana's Sons",
                "10.90 - Summary of Lord Krishna's Glories",
              ], [
                "11.01 - The Curse Upon the Yadu Dynasty",
                "11.02 - Maharaja Nimi Meets the Nine Yogendras",
                "11.03 - Liberation from the Illusory Energy",
                "11.04 - Drumila Explains the Incarnations of Godhead to King Nimi",
                "11.05 - Narada Concludes His Teachings to Vasudeva",
                "11.06 - The Yadu Dynasty Retires to Prabhasa",
                "11.07 - Lord Krishna Instructs UddhavaThe Story of Pingala",
                "11.08 - The Story of Pingala",
                "11.09 - Detachment from All that Is Material",
                "11.10 - The Nature of Fruitive Activity",
                "11.11 - The Symptoms of Conditioned and Liberated Living Entities",
                "11.12 - Beyond Renunciation and Knowledge",
                "11.13 - The Hamsa-avatara Answers Questions of the Sons of Brahma",
                "11.14 - Lord Krishna Explains the Yoga System to Sri Uddhava",
                "11.15 - Lord Krishna's Description of Mystic Yoga Perfections",
                "11.16 - The Lord's Opulence",
                "11.17 - Lord Krishna's Description of the Varnasrama Systems",
                "11.18 - Description of Varnasrama-dharma",
                "11.19 - The Perfection of Spiritual Knowledge",
                "11.20 - Devotional Service Surpasses Knowledge and Detachment",
                "11.21 - Lord Krishna's Explanation of the Vedic Path",
                "11.22 - Enumeration of the Elements of Material Creation",
                "11.23 - The Song of the Avanti Brahmana",
                "11.24 - The Philosophy of Sankhya",
                "11.25 - The Three Modes of Nature and Beyond",
                "11.26 - The Aila-gita",
                "11.27 - Krishna's Instructions on the Process of Deity Worship",
                "11.28 - Jnana-yoga",
                "11.29 - Bhakti-yoga",
                "11.30 - The Disappearance of the Yadu Dynasty",
                "11.31 - The Disappearance of Lord Sri Krishna",
              ], [
                "12.01 - The Degraded Dynasties of Kali-yuga",
                "12.02 - The Symptoms of Kali-yuga",
                "12.03 - The Bhumi-gita",
                "12.04 - The Four Categories of Universal Annihilation",
                "12.05 - Sri Suka's Final Instructions to Maharaja Parikshit",
                "12.06 - Maharaja Pariksit Passes Away",
                "12.07 - The Puranic Literatures",
                "12.08 - Markandeya's Prayers to Nara-Narayana Rishi",
                "12.09 - Markandeya Rishi Sees the Illusory Potency of the Lord",
                "12.10 - Lord Siva and Uma Glorify Markandeya Rishi",
                "12.11 - Summary Description of the Mahapurusa",
                "12.12 - The Topics of Srimad-Bhagavatam Summarized",
                "12.13 - The Glories of Srimad-Bhagavatam"
              ]]
    if canto < 0 or chapter < 0 or canto >= len(titles) or canto >= len(titles[canto]):
        return "Canto passed is %02d and Chapter passed is %02d. Canto and Chapter is out of range" % (canto, chapter)

    return re.sub(r'\d+\.\d+\s-\s(.*)', r'\1', titles[canto][chapter])

def updateDasamaskandamVideoTags(videoId=None, videoNumber=None, categoryId=10, canto=10, playlistId="PLdBTiOEoG70mV-0PAAG5NFWiXGFZy1inB", fromItem=None, toItem=None):
    adhyayam_number=1
    with build('youtube', 'v3', static_discovery=False, credentials=getCredentials()) as service:
        playlist = []
        try:
            if videoNumber != None:
                adhyayam_number=videoNumber
            if videoId != None:
                playlist.append({'videoId': videoId})
            else:
                if not os.path.exists("videosInPlayList-"+playlistId+".json"):
                    listPlaylistItems(playlistId=playlistId)
                with open("videosInPlayList-"+playlistId+".json", "r", encoding="UTF-8") as f:
                    playlist = json.load(f)

            response_file = open("response_"+time.strftime("%Y%m%d%H%M%S",
                                 time.localtime())+".json", "wt", encoding="UTF-8")
            response_file.write("[\n")
            playlistItem=0
            for video in playlist:
                if (fromItem == None or (fromItem != None and playlistItem+1 > fromItem)) and (toItem == None or (toItem != None and playlistItem+1 < toItem)):
                    if video['videoId'] != None:
                        videoCategoryId = categoryId
                        videoTitle = 'Srimad Bhagavatham Canto ' + str(canto).zfill(2) + ' Chapter ' + str(adhyayam_number).zfill(2) + " | " + get_title(canto-1,adhyayam_number-1)
                        print(videoTitle)
                        videoCategoryId = 10
                        videoDescription = """
#SrimadBhagavatham #MahaPuran #MythiliRajaraman

%s

Canto 01 Playlist: https://www.youtube.com/playlist?list=PLdBTiOEoG70lFwr8HD1X-f-X965AkQetE
Canto 02 Playlist: https://www.youtube.com/playlist?list=PLdBTiOEoG70nrGqDyA1AQvvZgRyPSmRoN
Canto 03 Playlist: https://www.youtube.com/playlist?list=PLdBTiOEoG70ktFSk5DXfEaFHUrNbs7i9B
Canto 10 Playlist: https://www.youtube.com/playlist?list=PLdBTiOEoG70mV-0PAAG5NFWiXGFZy1inB
""" % ('Srimad Bhagavatham Skandam ' + str(canto).zfill(2) + ' Adhyayam ' + str(adhyayam_number).zfill(2) + " - " + get_title(canto-1,adhyayam_number-1))
                        print(videoDescription)

                        # Update Tag of a video
                        request = service.videos().update(
                            part="snippet",
                            body={
                                "id": video['videoId'],
                                "snippet": {
                                    "categoryId": videoCategoryId,
                                    "tags": [
                                        "Srimad Bhagavatam",
                                        "Srila Prabhupada",
                                        "Krishna premi",
                                        "BLISS",
                                        "Bhaktivedanta",
                                        "Dictations",
                                        "Recordings",
                                        "chanting",
                                        "audible",
                                        "audio book",
                                        "mantra",
                                        "sukadeva goswami",
                                        "bagavatam",
                                        "bagavatham",
                                        "bhagavatam",
                                        "bhagavatham",
                                        "krishna",
                                        "canto " + str(canto).zfill(2),
                                        "chapter " + str(adhyayam_number).zfill(2),
                                        "Srimad bhagavatham"
                                    ],
                                    "title": videoTitle,
                                    "description": videoDescription
                                }
                            }
                        )
                        response = request.execute()
                        response_file.write(json.dumps(response, indent=2))
                        response_file.write(",\n")
                        adhyayam_number += 1
                playlistItem+=1
            response_file.write("]\n")
            response_file.close()
        except requests.HTTPError as e:
            print('Error response status code : {0}, reason : {1}'.format(
                e.status_code, e.error_details))

def updatePillaiTamil():
    categoryId=10
    with build('youtube', 'v3', static_discovery=False, credentials=getCredentials()) as service:
        playlist = []
        try:
            with open("videosInPlayList-pillaitamil.json", "r", encoding="UTF-8") as f:
                playlist = json.load(f)

            response_file = open("response_"+time.strftime("%Y%m%d%H%M%S",
                                 time.localtime())+".log", "wt", encoding="UTF-8")
            response_file.write("[\n")
            for video in playlist:
                videoCategoryId = categoryId
                videoTitle = video['title']
                videoDescription = """
#PillaiTamil #SriSriAnna #MythiliRajaraman

%s

Pillai tamil on Sri Sri Krishna Premi Swamigal, fondly called as SriSriAnna by his devotees.

These songs have been composed by Smt. Sivakamu Krishnadas

Full Playlist: https://www.youtube.com/playlist?list=PLdBTiOEoG70lV15Qacf-ctJbMmz79hBQY

""" % (video['title'])

                request = service.videos().update(
                    part="snippet",
                    body={
                        "id": video['videoId'],
                        "snippet": {
                            "categoryId": videoCategoryId,
                            "tags": [
                                "premi",
                                "anna",
                                "bhajan",
                                "lyrics",
                                "tamil",
                                "krishnapremi",
                                "pillai"
                            ],
                            "title": videoTitle,
                            "description": videoDescription
                        }
                    }
                )
                response = request.execute()
                response_file.write(json.dumps(response, indent=2))
                response_file.write(",\n")
                time.sleep(5) #delay 1 second to catchup
            response_file.write("]\n")
            response_file.close()
        except requests.HTTPError as e:
            print('Error response status code : {0}, reason : {1}'.format(
                e.status_code, e.error_details))


def initialize_upload(youtube, options):
    tags = None
    if options.keywords:
        tags = options.keywords.split(",")

    body = dict(
        snippet=dict(
            title=options.title,
            description=options.description,
            tags=tags,
            categoryId=options.category
        ),
        status=dict(
            privacyStatus=options.privacyStatus
        )
    )

    # Call the API's videos.insert method to create and upload the video.
    insert_request = youtube.videos().insert(
        part=",".join(body.keys()),
        body=body,
        # The chunksize parameter specifies the size of each chunk of data, in
        # bytes, that will be uploaded at a time. Set a higher value for
        # reliable connections as fewer chunks lead to faster uploads. Set a lower
        # value for better recovery on less reliable connections.
        #
        # Setting "chunksize" equal to -1 in the code below means that the entire
        # file will be uploaded in a single HTTP request. (If the upload fails,
        # it will still be retried where it left off.) This is usually a best
        # practice, but if you're using Python older than 2.6 or if you're
        # running on App Engine, you should set the chunksize to something like
        # 1024 * 1024 (1 megabyte).
        media_body=MediaFileUpload(options.file, chunksize=-1, resumable=True)
    )

    resumable_upload(insert_request)

# This method implements an exponential backoff strategy to resume a
# failed upload.


def resumable_upload(insert_request):
    response = None
    error = None
    retry = 0
    while response is None:
        try:
            print("Uploading file...")
            status, response = insert_request.next_chunk()
            if response is not None:
                if 'id' in response:
                    print("Video id '%s' was successfully uploaded." %
                          response['id'])
                else:
                    exit("The upload failed with an unexpected response: %s" % response)
        except requests.HTTPError as e:
            if e.resp.status in RETRIABLE_STATUS_CODES:
                error = "A retriable HTTP error %d occurred:\n%s" % (e.resp.status,
                                                                     e.content)
            else:
                raise
        except RETRIABLE_EXCEPTIONS as e:
            error = "A retriable error occurred: %s" % e

        if error is not None:
            print(error)
            retry += 1
            if retry > MAX_RETRIES:
                exit("No longer attempting to retry.")

            max_sleep = 2 ** retry
            sleep_seconds = random.random() * max_sleep
            print("Sleeping %f seconds and then retrying..." % sleep_seconds)
            time.sleep(sleep_seconds)


if __name__ == '__main__':
    argparser = argparse.ArgumentParser(description='Process some integers.')
    argparser.add_argument("--file", required=True,
                           help="Video file to upload")
    argparser.add_argument("--title", help="Video title", default="Test Title")
    argparser.add_argument("--description", help="Video description",
                           default="Test Description")
    argparser.add_argument("--category", default="10",
                           help="Numeric video category. " +
                           "See https://developers.google.com/youtube/v3/docs/videoCategories/list")
    argparser.add_argument("--keywords", help="Video keywords, comma separated",
                           default="")
    argparser.add_argument("--privacyStatus", choices=VALID_PRIVACY_STATUSES,
                           default=VALID_PRIVACY_STATUSES[0], help="Video privacy status.")
    args = argparser.parse_args(['--file','adhyanam48.mp4'])

    #print(args)

#updateVideoTags(videoId=None, playlistId="PLdBTiOEoG70mV-0PAAG5NFWiXGFZy1inB")
#print(json.dumps(readVideoDetails("CUhx8EhI-gE"), indent=2))
#enrichDuration("PLdBTiOEoG70n_aTSZgIGi3pOtyO7D2Tky")
#updateRSVideoTags()
#listPlaylistItems("PLmozlYyYE-ERAkAKl-MbnQal-49xPVNwn")
#updateDasamaskandamVideoTags(playlistId="PLdBTiOEoG70mV-0PAAG5NFWiXGFZy1inB", canto=10)
updatePillaiTamil()
