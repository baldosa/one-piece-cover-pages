# striped down from https://github.com/eshmu/gphotos-upload

from __future__ import print_function
import json
import os.path
from google.auth.transport.requests import AuthorizedSession
import os.path
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import AuthorizedSession

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/photoslibrary',
          'https://www.googleapis.com/auth/photoslibrary.appendonly',
          'https://www.googleapis.com/auth/photoslibrary.sharing']


def auth():
    """Shows basic usage of the Drive v3 API.
    Prints the names and ids of the first 10 files the user has access to.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'client_id.json', SCOPES)
            creds = flow.run_console(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    session = AuthorizedSession(creds)
    return session


def upload_photos(session, photo_file_name, album_id):

    session.headers["Content-type"] = "application/octet-stream"
    session.headers["X-Goog-Upload-Protocol"] = "raw"

    try:
        with open(photo_file_name, mode='rb') as photo_file:
            photo_bytes = photo_file.read()

            session.headers["X-Goog-Upload-File-Name"] = os.path.basename(
                photo_file_name)

            upload_token = session.post(
                'https://photoslibrary.googleapis.com/v1/uploads', photo_bytes)

            if (upload_token.status_code == 200) and (upload_token.content):

                create_body = json.dumps({"albumId": album_id, "newMediaItems": [
                                         {"description": "", "simpleMediaItem": {"uploadToken": upload_token.content.decode()}}]}, indent=4)

                resp = session.post(
                    'https://photoslibrary.googleapis.com/v1/mediaItems:batchCreate', create_body).json()

                # print("Server response: {}".format(resp))

                if "newMediaItemResults" in resp:
                    status = resp["newMediaItemResults"][0]["status"]
                    if status.get("code") and (status.get("code") > 0):
                        print("Could not add \'{0}\' to library -- {1}".format(
                            os.path.basename(photo_file_name), status["message"]))
                    else:
                        print(f"Uploaded {os.path.basename(photo_file_name)}")
                else:
                    print("Could not add \'{0}\' to library. Server Response -- {1}".format(
                        os.path.basename(photo_file_name), resp))

            else:
                print("Could not upload \'{0}\'. Server Response - {1}".format(
                    os.path.basename(photo_file_name), upload_token))

    except OSError as err:
        print('error')

    try:
        del(session.headers["Content-type"])
        del(session.headers["X-Goog-Upload-Protocol"])
        del(session.headers["X-Goog-Upload-File-Name"])
    except KeyError:
        pass
