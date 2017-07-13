import requests
from bs4 import BeautifulSoup


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
