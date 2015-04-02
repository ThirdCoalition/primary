from django.shortcuts import render, redirect

from datetime import datetime

from primary.models import Candidate, Vote, Approval, Sums
from models import Visit

def sections():
    return [{'title': 'Primary', 'location': '/'},
            {'title': 'Help Wanted', 'location': '/help'},
            {'title': 'About Us', 'location': '/about'},
            {'title': 'Electoral Reform', 'location': '/reform'},
            {'title': 'Related Organizations', 'location': '/related'},
            {'title': 'News', 'location': '/news'},
            {'title': 'Blog', 'location': '/blog'},
            {'title': 'Contact', 'location': '/contact'}]

def full_context():
    return {'sections': sections(), 'candidates': Candidate.objects.all()}

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def record_visit(request, section, arg=""):
    Visit(ip=get_client_ip(request), time=datetime.now(), page=section, arg=arg).save()

def record_ratings(request):
    vote = Vote(ip=get_client_ip(request), time=datetime.now())
    vote.save()
    approvals = []
    total = 0

    # TODO: Less slacker validation
    for key in request.POST:
        try:
            id = int(key)
            rating = int(request.POST[key])
        except ValueError:
            continue

        if rating > 10:
            continue

        total += rating
        approvals += [Approval(rating=rating, candidate=Candidate.objects.get(id=id), vote=vote)]

    # Spammers may try naively submitting 10/0/0/0 ratings.
    # This is not real spam protection, but let's pretend to accept the submissions.
    # Considering we are open source, if someone really wants to spam it will not take long to figure out.
    # TODO: Actual spam protection
    if total >= 15:
        map(lambda a: a.save(), approvals)

def get_percentages():
    ratings = Sums.objects.all()
    total = sum(map(lambda r: r.approval, ratings))
    for rating in ratings:
        rating.approval = 100 * rating.approval / total

        # arbitrary scaling factor and minimum width
        setattr(rating, 'display_width', rating.approval * 20 + 40)

    return ratings

def primary(request):
    record_visit(request, 'primary')
    return render(request, 'primary.html', dict(full_context(),
                                                ratings = get_percentages(),
                                                saved = ('saved' in request.GET)))

def vote(request):
    record_visit(request, 'vote')
    return render(request, 'vote.html', full_context())

def range(request):
    record_visit(request, 'range', request.GET['name'])
    return render(request, 'range.html', dict(full_context(), fav=Candidate.objects.get(name=request.GET['name'])))

def saverange(request):
    record_visit(request, 'saverange')
    record_ratings(request)

    return redirect("/?saved")

def help(request):
    record_visit(request, 'help')
    return render(request, 'help.html', full_context())

def about(request):
    record_visit(request, 'about')
    return render(request, 'about.html', full_context())

def reform(request):
    record_visit(request, 'reform')
    return render(request, 'reform.html', full_context())

def related(request):
    record_visit(request, 'related')
    return render(request, 'related.html', full_context())

def freechange(request):
    record_visit(request, 'freechange')
    return render(request, 'freechange.html', full_context())

def news(request):
    record_visit(request, 'news')
    return render(request, 'news.html', full_context())

def blog(request):
    record_visit(request, 'blog')
    return render(request, 'blog.html', full_context())

def contact(request):
    record_visit(request, 'contact')
    return render(request, 'contact.html', full_context())
