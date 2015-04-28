from django.contrib.auth.models import User
from django.db import models

class Region(models.Model):
    name = models.CharField(max_length=20)

class Candidate(models.Model):
    region = models.ForeignKey(Region)
    name = models.CharField(max_length=30)
    synopsis = models.CharField(max_length=500)
    logo = models.URLField()
    link = models.URLField()
    color = models.CharField(max_length=30)
    fgcolor = models.CharField(max_length=30)
    shame = models.BooleanField(default=False)

class Approval(models.Model):
    user = models.ForeignKey(User)
    rating = models.IntegerField()
    candidate = models.ForeignKey(Candidate)

class UserSettings(models.Model):
    user = models.ForeignKey(User)
    region = models.ForeignKey(Region)
    delegate = models.ForeignKey(User, related_name="delegate")
    location = models.CharField(max_length=10, default='')
    handle = models.CharField(max_length=20, default='')

# This is a view. Not entirely sure why candi_id and candi_ptr_id are both required
## create view primary_sums as select primary_candidate.id as candidate_id, primary_candidate.id as candidate_ptr_id, sum(coalesce(rating, 0)) as approval from primary_candidate left outer join primary_approval on (primary_candidate.id = primary_approval.candidate_id) group by primary_candidate.id
class Sums(Candidate):
    approval = models.IntegerField()
    candidate = models.ForeignKey(Candidate, related_name='+')

    class Meta:
        managed = False
        ordering = ['-approval']
