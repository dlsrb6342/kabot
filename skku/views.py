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
    
    def delete(self, request):
        user_key = request.data.get('user_key')
        user = User.objects.get(user_key=user_key)
        user.last_visit = datetime.now()
        user.save()


class Friend(APIView):
    
    def post(self, request):
        user_key = request.data.get('user_key')
        user, created = User.objects.get_or_create(user_key=user_key)
        if not created:
            user.active = True
        user.save()

    def delete(self, request):
        user_key = request.data.get('user_key')
        user = User.objects.get(user_key=user_key)
        user.active = False
        user.save()


class Message(APIView):
    
    def post(self, request):
        user_key = request.data.get('user_key')
        content = request.data.get('content')
        if content == "대화 시작하기":
            return Response(dict(message=dict(text="학사일정이나 공식 메뉴를 물어봐주세요!")))
        user, created = User.objects.get_or_create(user_key=user_key)
        chat = Chat.objects.create(user=user, content=content)
        chat.save()
        category = cache.get(user_key)
        if category is None:
            category = extract_category(user_key, content)
            if category is None:
                return Response(ERROR_MESSAGE)

        flag, keyword = extract_keyword(category, content)
        if not flag:
            return Response(keyword)
        return Response(make_message(user_key, keyword))
