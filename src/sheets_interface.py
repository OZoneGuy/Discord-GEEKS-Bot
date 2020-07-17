from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import json
import sql_handler
from bot_utils import get_config

SCOPES = 'https://www.googleapis.com/auth/spreadsheets.readonly'
config = json.load(open(get_config()))

sheet_ID = config['sheet_id']
sheet_range = 'A2:F'


def main():
    store = file.Storage('data/token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('data/google-sheets-credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('sheets', 'v4', http=creds.authorize(Http()))

    result = service.spreadsheets().values().get(spreadsheetId=sheet_ID,
                                                 range=sheet_range).execute()
    values = result.get('values', [])

    if not values:
        print('No data found.')
    else:
        for row in values:
            try:
                sql_handler.insert_form_response(row[0], row[1], row[2], True if row[3] == 'Yes' else False, row[4], row[5])
            except:
                print('error')

            pass


if __name__ == '__main__':
    main()
