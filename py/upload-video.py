import http.client
import httplib2
import requests
import random
import os
import time
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import os
import sys
from os import path

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

def getCredentials():
    credentials = None

    if os.path.exists("../automate-youtube/token.pickle"):
        with open("../automate-youtube/token.pickle", "rb") as token:
            credentials = pickle.load(token)

    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "../automate-youtube/client_secrets.json", scopes=[
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
        with open("../automate-youtube/token.pickle", "wb") as token:
            pickle.dump(credentials, token)
        # print(credentials.to_json())
    return credentials

def upload_video(dashakam_number):
    ASTRING='Narayaneeyam-' + dashakam_number.zfill(3)
    video_file = ASTRING + ".mp4"
    thumbnail = ASTRING + "-Slide0001.jpg"
    print("Inside upload_video. video_file = " + video_file)

    body = dict(
        snippet=dict(
            title="Narayaneeyam Dashakam %s" % (dashakam_number.zfill(3)),
            description="""#Narayaneeyam #mythilirajaraman #krishnaleelai
Narayaneeyam Dashakam %s
Playlist https://www.youtube.com/playlist?list=PLdBTiOEoG70lyLxcUM02RHJ3W5SdMbRf8
            """ % (dashakam_number.zfill(3)),
            tags=["Srimad Bhagavatam",
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
                  "dashakam " + str(dashakam_number).zfill(3),
                  "chapter " + str(dashakam_number).zfill(3),
                  "Srimad bhagavatham"
                 ],
            categoryId=10
        ),
        status=dict(
            privacyStatus="unlisted"
        )
    )

    with build('youtube', 'v3', static_discovery=False, credentials=getCredentials()) as service:
        try:
            # Call the API's videos.insert method to create and upload the video.
            insert_request = service.videos().insert(
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
                media_body=MediaFileUpload(video_file, chunksize=-1, resumable=True)
            )

            uploaded_video_id = resumable_upload(insert_request)
            print('Setting thumbnail as ' + thumbnail)
            request = service.thumbnails().set(videoId=uploaded_video_id,media_body=MediaFileUpload(thumbnail))
            response = request.execute()
            print('Response for setting thumbnail: ')
            print(response)
            if input ("Add to Playlist(y/n)? : ") == 'y':
                insert_playlistitem('PLdBTiOEoG70lyLxcUM02RHJ3W5SdMbRf8', uploaded_video_id)
        except requests.HTTPError as e:
            print('Error response status code : {0}, reason : {1}'.format(
                e.status_code, e.error_details))

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
                    print("Video id '%s' was successfully uploaded." % response['id'])
                    return response['id']
                else:
                    print("The upload failed with an unexpected response: %s" % response)
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
                print("No longer attempting to retry.")

            max_sleep = 2 ** retry
            sleep_seconds = random.random() * max_sleep
            print("Sleeping %f seconds and then retrying..." % sleep_seconds)
            time.sleep(sleep_seconds)
    return None

def insert_playlistitem(playlistIdStr, videoIdStr):
    with build('youtube', 'v3', static_discovery=False, credentials=getCredentials()) as service:
        print('Adding to playlist')
        body=dict(
            snippet=dict(
                playlistId=playlistIdStr,
                resourceId=dict(
                    kind='youtube#video',
                    videoId=videoIdStr
                )
            )
        )
        print(body)
        insert_request = service.playlistItems().insert(
                            part=",".join(body.keys()),
                            body=body
                         )
        response = insert_request.execute()
        print('Response for adding to playlist: ')
        print(response)

#
# Main Code Starts
#
if len(sys.argv) != 2:
  file_dashakam_number=""
  if path.exists("dashakam_number.txt"):
    f=open("dashakam_number.txt")
    file_dashakam_number = f.readlines()[0]
    f.close()
  dashakam_number = input ("Dashakam Number?(" + file_dashakam_number + "): ")
  if dashakam_number == "" and file_dashakam_number != "":
    dashakam_number = file_dashakam_number
else:
  dashakam_number = sys.argv[1]
      
f=open("dashakam_number.txt", "w")
f.write(dashakam_number)
f.close()

upload_video(dashakam_number)
input("Press enter to continue...")
