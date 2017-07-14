from skku.models import ERROR_MESSAGE
from utils.get_meal import *
from utils.get_schedule import get_schedule
from django.core.cache import cache

def make_message(user_key, keyword):
    category = cache.get(user_key)
    cache.delete(user_key)
    message = dict(message=dict(text=""))

    if category.name == "공식":
        message['message']['text'] = gongsik(keyword)
    elif category.name == "일정" or category.name == "언제":
        message['message']['text'] = schedule(keyword)

    if message['message']['text'] == "":
        return ERROR_MESSAGE
    return message


def gongsik(keyword):
    menu = get_gongsik()
    if menu is None:
        return "오늘은 쉬는 날인가봐요! 메뉴 정보가 없네요ㅠㅠ"
    temp = ["아침", "점심", "저녁"]
    time = ["조식", "중식", "석식"]

    for i in range(3):
        if temp[i] in keyword:
            keyword.remove(temp[i])
            keyword.append(time[i])

    answer = ""
    for t in time:
        if t in keyword:
            answer += "\r\n" + t +"\n"
            for m in menu[t]:
                answer += m + "\n"
    return answer


def schedule(keyword):
    schedule_list = get_schedule()
    answer = ""
    answer_dic = {}
    first = False
    for k in keyword:
        for schedule in schedule_list:
            if k in schedule[0] and not schedule[1] in answer_dic:
                if first:
                    answer += "\r\n\r\n"
                first = True
                answer_dic[schedule[1]] = schedule[0]
                answer += schedule[0] + "  -  " + schedule[1]
