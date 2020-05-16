import json
from datetime import datetime


def get_message_from_json(data: str) -> str:
    messages: dict = json.load(open('messages.json'))
    return messages[data]


def write_log(text: str) -> None:
    text = str(datetime.now()) + " - " + text + "\n"
    f = open("GEEK.log", "a+")
    f.write(text)
    f.close()
