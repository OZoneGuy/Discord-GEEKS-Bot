import csv
from json import load
from urllib.request import urlopen
from os import remove

from sql_handler import insert_form_response
from bot_utils import get_config


def import_form():
    config = load(open(get_config()))
    DATA_F_NAME = "entries.csv"

    sheet_ID = config['sheet_id']
    response = urlopen("https://docs.google.com/spreadsheets/"
                       "d/" + sheet_ID + "/"
                       "export?format=csv", timeout=5)

    with open(DATA_F_NAME, 'wb') as f:
        f.write(response.read())

    with open(DATA_F_NAME, 'r') as f:
        csv_file = csv.reader(f)
        for row in csv_file:
            try:
                insert_form_response(row[0], row[1], row[2],
                                     True if row[3] == 'Yes'
                                     else False, row[4], row[5])
            except Exception():
                print('error')

    remove(DATA_F_NAME)
