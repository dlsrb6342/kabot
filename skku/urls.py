from django.conf.urls import url
from skku import views


urlpatterns = [
    url(r'^keyboard$', views.HomeKeyboard.as_view()),
    url(r'^friend$', views.Friend.as_view()),
    url(r'^message$', views.Message.as_view()),
]
