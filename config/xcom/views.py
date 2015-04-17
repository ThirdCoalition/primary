from django.shortcuts import render, redirect

from datetime import datetime
from random import shuffle

from primary.models import Candidate, Vote, Approval, Sums
from models import Visit

def sections():
    return [{'title': 'Primary', 'location': '/'},
            {'title': 'Platform', 'location': '/platform'},
            {'title': 'Parties', 'location': '/parties'},
            {'title': 'NPOs', 'location': '/npos'},
            {'title': 'About', 'location': '/about'}]

def almanacs():
    return [[dict(title="Foundations", location="foundations"),
             dict(title="Brain Train", location="braintrain"),
             dict(title="Wikis (back-story)", location="wayback"),
             dict(title="There and Back", location="thereandback"),
             dict(title="Infrastructure", location="infrastructure"),
             dict(title="Memory", location="memory"),
             dict(title="Disobedience", location="disobedience"),
             dict(title="Meme Theory", location="meme"),
             dict(title="Signs", location="signs")],
            [dict(title="Ouroboros", location="ouroboros"),
             dict(title="Labyrinths", location="labyrinths"),
             dict(title="Guides", location="guides"),
             dict(title="Compendiums", location="compendiums"),
             dict(title="Simulacra", location="simulacra"),
             dict(title="CS", location="cs"),
             dict(title="Very Small", location="verysmall"),
             dict(title="Universal", location="universal"),
             dict(title="Kafkaesque", location="kafkaesque"),
             dict(title="Sedaris", location="sedaris")]]

def full_context():
    return {'sections': sections()}

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

    for key in request.POST:
        try:
            id = int(key)
            rating = int(request.POST[key])
        except ValueError:
            continue

        if rating > 10 or rating < 0:
            continue

        total += rating
        approvals += [Approval(rating=rating, candidate=Candidate.objects.get(id=id), vote=vote)]

    # favorite is allowed 5 points + 1 point for each non-favorite approval point
    favorite = max(map(lambda a:a.rating, approvals))
    if min(5, (total - 5) / 2) == favorite - 5:
        map(lambda a: a.save(), approvals)

def get_percentages():
    ratings = Sums.objects.all()
    total = max(sum(map(lambda r: r.approval, ratings)), 1)
    for rating in ratings:
        rating.approval = 100 * rating.approval / total

        # arbitrary scaling factor and minimum width
        setattr(rating, 'display_width', min(25, max(2, rating.approval)) * 20)

    return sorted(ratings, key=lambda rating: rating.candidate.shame, reverse=True)

def get_ballot():
    percentages = get_percentages()
    return sorted(map(lambda rating: rating.candidate,
                      sorted(percentages, key=lambda rating: rating.approval, reverse=True)),
                  key=lambda candidate: candidate.shame)

def primary(request):
    record_visit(request, 'primary')
    return render(request, 'primary.html', dict(full_context(),
                                                ratings = get_percentages(),
                                                numvotes = Vote.objects.count(),
                                                saved = ('saved' in request.GET)))

def vote(request):
    record_visit(request, 'vote')
    return render(request, 'vote.html', dict(full_context(), candidates = get_ballot()))

def random(request):
    record_visit(request, 'random')

    candidates = get_ballot()
    shuffle(candidates)
    return render(request, 'vote.html', dict(full_context(), candidates=candidates))

def range(request):
    record_visit(request, 'range', request.GET['fav'])
    return render(request, 'range.html', dict(full_context(), fav=Candidate.objects.get(name=request.GET['fav']),
                                              candidates = get_ballot()))

def approval(request):
    record_visit(request, 'approval', request.GET['fav'])
    return render(request, 'approval.html', dict(full_context(), fav=Candidate.objects.get(name=request.GET['fav']),
                                                 candidates = get_ballot()))

def saverange(request):
    record_visit(request, 'saverange')
    record_ratings(request)

    return redirect("/?saved")

def about(request):
    record_visit(request, 'about')
    return render(request, 'about.html', full_context())

def npos(request):
    record_visit(request, 'npos')
    return render(request, 'npos.html', full_context())

def platform(request):
    record_visit(request, 'platform')
    return render(request, 'platform.html', full_context())

def parties(request):
    record_visit(request, 'parties')
    return render(request, 'parties.html', full_context())
