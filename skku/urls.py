from django.conf.urls import url
from skku import views


urlpatterns = [
    url(r'^keyboard$', views.HomeKeyboard.as_view()),
    url(r'^friend$', views.FriendAdd.as_view()),
    url(r'^friend/(?P<user_key>[0-9a-zA-Z-]+)/$', views.FriendDelete.as_view()),
    url(r'^message$', views.Message.as_view()),
    url(r'^chat_room/(?P<user_key>[0-9a-zA-Z-]+)/$', views.Exit.as_view()),
]
