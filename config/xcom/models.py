from django.db import models

class Visit(models.Model): #TODO: Install proper analytics framework
    ip = models.GenericIPAddressField()
    time = models.TimeField()
    page = models.CharField(max_length=30)
    arg = models.CharField(max_length=30)
