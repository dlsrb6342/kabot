from django.db import models


class User(models.Model):
    CAMPUS_LIST = (
        ('M', '인문사회과학캠퍼스'),
        ('Y', '자연과학캠퍼스')
    )

    user_key = models.CharField(max_length=100)
    last_visit = models.DateField(auto_now_add=True, blank=True)
    active = models.BooleanField(default=True)
    campus = models.CharField(null=True, choices=CAMPUS_LIST)

class Chat(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateField(auto_now_add=True, blank=True)


