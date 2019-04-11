from django.db import models
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill
from django.conf import settings

# Create your models here.
class Post(models.Model):
    content = models.CharField(max_length=100)
    # image = models.ImageField(blank = True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE) # user를 변수화해서 넣음.
    # 1:N 관계(사용자 한명이 자기가 쓴 게시물을 여러개 가질 수 있다 -> on_delete=models.CASCADE 필요함)

        
class Image(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    file = ProcessedImageField(
        upload_to = 'posts/images', # 저장위치
        processors = [ResizeToFill(600,600)], # 크기지정
        format = 'JPEG',
        options = {'quality':90},
        )
        
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE) # user한명이 comment 여러개 작성 가능
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    
    