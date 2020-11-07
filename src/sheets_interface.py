from __future__ import print_function

import json
import os.path
import pickle

import sql_handler
from bot_utils import get_config
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = 'https://www.googleapis.com/auth/spreadsheets.readonly'
config = json.load(open(get_config()))

sheet_ID = config['sheet_id']
sheet_range = 'A2:F'

TOKEN_PATH = 'data/token.pickle'
CRED_PATH = 'data/credentials.json'


def main():
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists(TOKEN_PATH):
        with open(TOKEN_PATH, 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                CRED_PATH, SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(TOKEN_PATH, 'wb') as token:
            pickle.dump(creds, token)

    service = build('sheets', 'v4', credentials=creds)

    result = service.spreadsheets().values().get(spreadsheetId=sheet_ID,
                                                 range=sheet_range).execute()
    values = result.get('values', [])

    if not values:
        print('No data found.')
    else:
        for row in values:
            try:
                sql_handler.insert_form_response(row[0], row[1], row[2],
                                                 True if row[3] == 'Yes'
                                                 else False, row[4], row[5])
            except Exception():
                print('error')


if __name__ == '__main__':
    main()
