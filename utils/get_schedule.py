from bs4 import BeautifulSoup
from datetime import datetime
import requests


def chunker(seq, size):
    return (seq[pos:pos + size] for pos in range(0, len(seq), size))


def get_schedule():
    SCHEDULE_LIST = []
    SCHEDULE_URL = "http://www.skku.edu/new_home/edu/bachelor/ca_de_schedule_"+ str(datetime.now().year) +".jsp"

    response = requests.get(SCHEDULE_URL)
    Soup = BeautifulSoup(response.text, 'html5lib')
    Schedules = Soup.find_all('td')

    for schedule in chunker(Schedules, 2):
        SCHEDULE_LIST.append((schedule[1].string.strip(), schedule[0].string.strip()))

    return SCHEDULE_LIST
