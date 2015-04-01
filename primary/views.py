from django.shortcuts import render
from django.http import HttpResponse

from primary.models import Candidate

def results(request):
    return render(request, 'index.html', Candidate.objects().all()
