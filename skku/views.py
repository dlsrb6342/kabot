from rest_framework.views import APIView
from rest_framework.response import Response
from datetime import datetime
from skku.models import *


class HomeKeyboard(APIView):
    
    def get(self, request):
        home_keyboard = {
            "type" : "buttons",
            "buttons" : ["캠퍼스 설정하기", "공지사항", ""]
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
        user = User.objects.get(user_key=user_key)
        chat = Chat.objects.create(user=user, content=content)
        chat.save()

