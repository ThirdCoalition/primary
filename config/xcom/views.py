from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from datetime import datetime
from random import shuffle

from primary.models import Candidate, Approval, Sums
from models import Visit

def sections():
    return [{'title': 'Primary', 'location': '/'},
            {'title': 'Platform', 'location': '/platform'},
            {'title': 'Regions', 'location': '/regions'},
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
    return
#    Visit(ip=get_client_ip(request), time=datetime.now(), page=section, arg=arg).save()

def record_ratings(request):
    fav_saved = False
    for key in request.POST:
        try:
            id = int(key)
            rating = int(request.POST[key])
        except ValueError:
            continue

        if rating > 10 or rating < 0:
            continue

        if rating == 10:
            if fav_saved:
                rating = 9
            else:
                fav_saved = True

        try:
            approval = Approval.objects.get(candidate=Candidate.objects.get(id=id), user=request.user)
            approval.rating = rating
            approval.save()
        except Approval.DoesNotExist:
            Approval(rating=rating, candidate=candi, user=request.user).save()
        except Candidate.DoesNotExist:
            continue

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
                                                numvotes = Approval.objects.filter(candidate_id=1).count(),
                                                voted = request.user.is_authenticated() and \
                                                    (Approval.objects.filter(user=request.user).count() > 0),
                                                saved = ('saved' in request.GET)))

@login_required(redirect_field_name=None)
def vote(request):
    record_visit(request, 'vote')
    return render(request, 'vote.html', dict(full_context(), candidates = get_ballot()))

@login_required(redirect_field_name=None)
def random(request):
    record_visit(request, 'random')

    candidates = get_ballot()
    shuffle(candidates)
    return render(request, 'vote.html', dict(full_context(), candidates=candidates))

@login_required(redirect_field_name=None)
def approval(request):
    candidates = get_ballot()
    for candi in candidates:
        rating = 0
        try:
            rating = Approval.objects.get(candidate=candi, user=request.user).rating
        except Approval.DoesNotExist:
            pass
        setattr(candi, 'rating', rating)
    
    fav = max(candidates, key=lambda candi: candi.rating)
    return render(request, 'approval.html', dict(full_context(), fav=fav, candidates = candidates))

@login_required(redirect_field_name=None)
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

def regions(request):
    record_visit(request, 'regions')
    return render(request, 'regions.html', full_context())
