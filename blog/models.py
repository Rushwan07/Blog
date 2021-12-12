from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.utils.timezone import now


class Post(models.Model):
    srn = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    content = models.TextField()
    author = models.CharField(max_length=12)
    views = models.IntegerField(default=0)
    slug = models.CharField(max_length=130)
    timeStamp = models.DateTimeField(blank=True)

    def __str__(self):
        return self.title + 'The Author is ' + self.author


class Comments(models.Model):
    sno = models.AutoField(primary_key=True)
    comment = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True)
    timestamp = models.DateTimeField(default=now)

    def __str__(self):
        return f"{self.sno}"
