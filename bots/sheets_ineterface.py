from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import json
import sql_handler

SCOPES = 'https://www.googleapis.com/auth/spreadsheets.readonly'
config = json.load(open('config.json'))

sheet_ID = config['sheet_id_test']
sheet_range = 'A2:F'


def main():
    store = file.Storage('token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('google-sheets-credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('sheets', 'v4', http=creds.authorize(Http()))

    result = service.spreadsheets().values().get(spreadsheetId=sheet_ID,
                                                 range=sheet_range).execute()
    values = result.get('values', [])

    if not values:
        print('No data found.')
    else:
        for row in values:
            sql_handler.insert_form_response(row[0], row[1], row[2], row[3], True if row[4] is 'Male' else False,
                                             row[5])
            pass


if __name__ == '__main__':
    main()
