
from django.shortcuts import render

from primary.models import Candidate

def home(request):
    return render(request, 'index.html', {'candidates': Candidate.objects.all()})

def vote(request):
    return render(request, 'vote.html', {'candidates': Candidate.objects.all()})

def help(request):
    return render(request, 'help.html')

def about(request):
    return render(request, 'about.html')

def reform(request):
    return render(request, 'reform.html')

def related(request):
    return render(request, 'related.html')

def freechange(request):
    return render(request, 'freechange.html')

def news(request):
    return render(request, 'news.html')

def blog(request):
    return render(request, 'blog.html')

def contact(request):
    return render(request, 'contact.html')
