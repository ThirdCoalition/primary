from django.db import models

class Candidate(models.Model):
    name = models.CharField(max_length=30)
    synopsis = models.CharField(max_length=500)
    logo = models.URLField()
    link = models.URLField()
    color = models.CharField(max_length=30)
