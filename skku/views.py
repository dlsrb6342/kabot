from rest_framework.views import APIView
from rest_framework.response import Response
from datetime import datetime
from skku.models import *
from django.core.cache import cache
from utils.extract_word import extract_category, extract_keyword
from utils.make_message import make_message


class HomeKeyboard(APIView):
    
    def get(self, request):
        home_keyboard = {
            "type" : "buttons",
            "buttons" : ["캠퍼스 설정하기", "대화 시작하기"]
        }
        return Response(home_keyboard)


class Exit(APIView):
    
    def delete(self, request, user_key):
        user = User.objects.get(user_key=user_key)
        user.last_visit = datetime.now()
        user.save()


class FriendAdd(APIView):
    
    def post(self, request):
        user_key = request.data.get('user_key')
        user, created = User.objects.get_or_create(user_key=user_key)
        if not created:
            user.active = True
        user.save()


class FriendDelete(APIView):

    def delete(self, request, user_key):
        user = User.objects.get(user_key=user_key)
        user.active = False
        user.save()


class Message(APIView):
    
    def post(self, request):
        user_key = request.data.get('user_key')
        content = request.data.get('content')
        campus_list = [ "인문사회과학캠퍼스", "자연과학캠퍼스" ]
        user, created = User.objects.get_or_create(user_key=user_key)
        last_visit = user.last_visit
        user.last_visit = datetime.now()
        if content == "캠퍼스 설정하기":
            cache.set(user_key + '_category', "campus")
            return Response({
                'message': {
                    'text': "캠퍼스를 선택해주세요!"
                }, 'keyboard': {
                    'type': "buttons",
                    'buttons': campus_list
                }
            })
        elif content in campus_list and cache.get(user_key + '_category') == "campus":
            user.campus = content
            user.save()
            cache.delete(user_key + '_category')
            return Response({
                'message': {
                    'text': content + "로 설정되었어요!"
                }, 'keyboard': {
                    "type" : "buttons",
                    "buttons" : ["캠퍼스 설정하기", "대화 시작하기"]
                }
            })
        elif content == "대화 시작하기":
            now = datetime.now()
            diff = now.day - last_visit.day
            text = "학사일정이나 공식, 긱식 메뉴를 물어봐주세요! 공식, 긱식 메뉴는 오늘 내일 메뉴를 알려줄 수 있어요!" + \
                    "\n예시 : '내일 점심 공식 메뉴 뭐야?'\n'등록금 납부 언제야?'\n'긱밥 점심 뭐야?'"
            if diff >= 4:
                text = str(diff) + "일만에 다시 오셨네요ㅎㅎ\r\n" + text
            return Response({
                "message": {
                    "text": text
                }
            })
        chat = Chat.objects.create(user=user, content=content)
        chat.save()
        category = cache.get(user_key + '_category')
        if category is None:
            category = extract_category(user_key, content)
            if category is None:
                return Response(ERROR_MESSAGE)

        flag, keyword = extract_keyword(category, content, user_key)
        if not flag:
            return Response(keyword)
        return Response(make_message(user_key, keyword))
