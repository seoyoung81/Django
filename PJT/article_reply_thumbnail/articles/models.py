from django.db import models
from imagekit.processors import Thumbnail, SmartResize,  ResizeToFill
from imagekit.models import ProcessedImageField, ImageSpecField

# Create your models here.
class Article(models.Model):
    title = models.CharField(max_length=30)
    content = models.TextField()
    image = models.ImageField(blank=True, null=True)
    thumbnail_img = ImageSpecField(
        source='thumbnail/',
        processors=[SmartResize(200, 300)],   # 200X300으로 줄이자.
        format='JPEG',
        options={'quality':80},
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.id}번째글 - {self.title}'

class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    content = models.CharField(max_length=200)
    parent  = models.ForeignKey('self', 
                                on_delete=models.CASCADE, 
                                null=True,
                                related_name='replies',
                                ) # 자기 자신 참조, 없으면 다 지우기, null 값이어도 괜찮, 겹칠수도 있으니 이름변경
