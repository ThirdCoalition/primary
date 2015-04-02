from django.core.management.base import BaseCommand
from datetime import datetime

from primary.models import Candidate, Vote, Approval, Sums

class Command(BaseCommand):

    help = "Initialize the voting record for ease of model programming"

    def handle(self, *args, **kwargs):
        vote = Vote(ip="0.0.0.0", time=datetime.now())
        vote.save()

        for c in Candidate.objects.all():
            Approval(rating=1, candidate=c, vote=vote).save()
