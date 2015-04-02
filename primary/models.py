from django.db import models

class Candidate(models.Model):
    name = models.CharField(max_length=30)
    synopsis = models.CharField(max_length=500)
    logo = models.URLField()
    link = models.URLField()
    color = models.CharField(max_length=30)
    fgcolor = models.CharField(max_length=30)

class Vote(models.Model):
    ip = models.GenericIPAddressField()
    time = models.TimeField()

class Approval(models.Model):
    rating = models.IntegerField()
    candidate = models.ForeignKey(Candidate)
    vote = models.ForeignKey(Vote)

#class Sums(Candidate):
#    approval = models.FloatField()
#    candidate = models.ForeignKey(Candidate)
#
#    class Meta:
#        managed = False
#        ordering = ['-approval']
