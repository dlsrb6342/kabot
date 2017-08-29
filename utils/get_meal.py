import requests
from bs4 import BeautifulSoup
from datetime import datetime


def get_gongsik():
    result = {}
    response = requests.get('http://www.skku.edu/new_home/campus/support/pop_menu1.jsp?restId=203')
    soup = BeautifulSoup(response.text, 'html5lib')
    notice_list = soup.find_all('p', class_='c_blue')
    if len(notice_list) == 0:
        return
    for notice in notice_list:
        if '휴무' in notice:
            return 

    for time in soup.findAll('h3'):
        meal_list = list()
        next_element = time
        while True:
            next_element = next_element.next
            if next_element.name == 'h2':
                result[time.img['alt']] = meal_list
                return result
            elif next_element.name == 'h3':
                result[time.img['alt']] = meal_list
                break
            elif next_element.name == 'h4':
                meal_list.append(next_element.text)


def get_giksik():
    day = str(datetime.today().day)
    month = str(datetime.today().month)
    year = str(datetime.today().year)
    result = {}
    response = requests.get('https://dorm.skku.edu/_custom/skku/_common/board/schedule_menu/food_menu_page.jsp?day=' +
                            day + '&month=' + month + '&year=' + year + '&board_no=61')
    soup = BeautifulSoup(response.text, 'html5lib')

    time = ["조식", "중식", "석식"]
    food_list = soup.findAll('div', class_='foodlist')

    for i in range(3):
        meal_list = list()
        for menu in food_list[i].findAll('p'):
            meal_list.append(menu.text.strip())
        result[time[i]] = meal_list
    return result