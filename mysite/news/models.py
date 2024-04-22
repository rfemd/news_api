from django.db import models
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from django.contrib.auth.models import User
import random
from django.template.defaultfilters import slugify
import uuid


class Tag(models.Model):
	title = models.CharField('Заголовок',max_length=200, blank=False)

	def __str__(self):
		return str(self.title)

	class Meta:
		ordering = ('title',)

class News(models.Model):
	#slug = models.SlugField(blank=True)
	title = models.CharField('Заголовок',max_length=200, blank=False,unique=True)
	text = models.TextField('Текст')
	picture = models.ImageField(default='news.jpg', upload_to='pictures/')
	tag = models.ForeignKey( Tag, on_delete=models.CASCADE, blank=True)
	likes = models.ManyToManyField(User, blank=True,related_name='likes')

	def __str__(self):
		return str(self.title)

	class Meta:
		ordering = ('tag',)

	def save(self, *args, **kwargs):
		#self.slug = slugify(self.title)
		return super().save(*args, **kwargs)

	def num_likes(self):
		return self.likes.all().count()

	

LIKE_CHOICES = (
    ('Like', 'Like'),
    ('Unlike', 'Unlike'),
)

class Like(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	news = models.ForeignKey(News, on_delete=models.CASCADE)
	value = models.CharField(choices=LIKE_CHOICES, max_length=8)
	def __str__(self):
		return str(self.value)
