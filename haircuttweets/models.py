from django.db import models

# Create your models here.

class TweetsSearched(models.Model):
	tweets_result = models.CharField(max_length=10*1024*1024, blank=True)