from django.db import models
from django.contrib.postgres.fields import JSONField, ArrayField


ERROR_MESSAGE = dict(message=dict(text="무슨 말씀이신 건가요? 다시 입력해주세요ㅠ"))


class User(models.Model):
    CAMPUS_LIST = (
        ('M', '인문사회과학캠퍼스'),
        ('Y', '자연과학캠퍼스')
    )

    user_key = models.CharField(max_length=100)
    last_visit = models.DateField(auto_now_add=True, blank=True)
    active = models.BooleanField(default=True)
    campus = models.CharField(null=True, max_length=10, choices=CAMPUS_LIST)


class Chat(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateField(auto_now_add=True, blank=True)


class Category(models.Model):
    name = models.CharField(max_length=100)
    arguments = ArrayField(JSONField(default={
        "type": "",
        "option": False,
        "error": ""
    }))


class Keyword(models.Model):
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=100)
