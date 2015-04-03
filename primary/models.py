from django.db import models

class Candidate(models.Model):
    name = models.CharField(max_length=30)
    synopsis = models.CharField(max_length=500)
    logo = models.URLField()
    link = models.URLField()
    color = models.CharField(max_length=30)
    fgcolor = models.CharField(max_length=30)
    shame = models.BooleanField(default=False)

class Vote(models.Model):
    ip = models.GenericIPAddressField()
    time = models.TimeField()

class Approval(models.Model):
    rating = models.IntegerField()
    candidate = models.ForeignKey(Candidate)
    vote = models.ForeignKey(Vote)

# This is a view. Not entirely sure why candi_id and candi_ptr_id are both required
# create view primary_sums as
# select candidate_id, candidate_id as candidate_ptr_id, sum(rating) as approval
#   from primary_approval
#   group by candidate_id
class Sums(Candidate):
    approval = models.IntegerField()
    candidate = models.ForeignKey(Candidate, related_name='+')

    class Meta:
        managed = False
        ordering = ['-approval']
