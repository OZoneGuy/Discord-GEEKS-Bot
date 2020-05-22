import json
import sys
from argparse import ArgumentParser as AP
from datetime import datetime


def get_message_from_json(data: str) -> str:
    messages: dict = json.load(open('messages.json'))
    return messages[data]


def write_log(text: str) -> None:
    text = str(datetime.now()) + " - " + text + "\n"
    f = open("GEEK.log", "a+")
    f.write(text)
    f.close()


def get_config() -> str:
    """
    Get the correct config file based on '--test' option
    """
    parser = AP()
    parser.add_argument('-t', '--test', action='store_true')
    name_s = parser.parse_args(sys.argv[1:])

    if name_s.test:
        print("Using test config")
        return "config_test.json"
    print("Using prod config")
    return "config.json"
