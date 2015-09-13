from django.db import models

# Create your models here.

class Persion(models.Model):
	puid = models.CharField(max_length=30)
	ppwd = models.CharField(max_length=30)
