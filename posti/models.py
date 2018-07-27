from datetime import datetime
from django.utils import timezone
from django_smalluuid.models import SmallUUIDField, uuid_default
from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class Post(models.Model):
    title = models.CharField(max_length=200, blank=False)
    text = models.TextField()
    uuid = SmallUUIDField(default=uuid_default())
    pub_date = models.DateTimeField('date published', default=timezone.now)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)

    @classmethod
    def create_post(self, title, text):
        posti = self(title=title, text=text)
        return posti

