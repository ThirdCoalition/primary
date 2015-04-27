from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.shortcuts import render, redirect

from datetime import datetime

from django.contrib.auth.models import User
from models import Candidate, Approval, UserSettings, Sums

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

def full_context(**kwargs):
    return dict({'sections': sections()}, **kwargs)

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def record_one_rating(request, candi_id, rating):
    candi = Candidate.objects.get(id=candi_id)
    try:
        approval = Approval.objects.get(candidate=candi, user=request.user)
        approval.rating = rating
        approval.save()
    except Approval.DoesNotExist:
        Approval(rating=rating, candidate=candi, user=request.user).save()

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

        record_one_rating(request, id, rating)

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

def user_voted(request):
    return Approval.objects.filter(user=request.user).count() > 0

def primary(request):
    return render(request, 'primary.html', 
                  full_context(ratings = get_percentages(),
                               # .distinct unavailable on sqlite3
                               numvotes = Approval.objects.values('user').annotate(Count('user')).count(),
                               voted = request.user.is_authenticated() and user_voted(request),
                               saved = ('saved' in request.GET)))

def vote(request):
    if not request.user.is_authenticated():
        return render(request, 'login.html', full_context(msg = 'vote'))
    
    if not user_voted(request) and 'fav' not in request.POST:
        return render(request, 'vote.html', full_context(candidates = get_ballot()))

    if 'fav' in request.POST:
        for approval in Approval.objects.filter(user=request.user):
            if approval.rating == 10:
                approval.rating = 9
                approval.save()

        record_one_rating(request, int(request.POST['fav']), 10)

    candidates = get_ballot()
    for candi in candidates:
        rating = 0
        try:
            rating = Approval.objects.get(candidate=candi, user=request.user).rating
        except Approval.DoesNotExist:
            pass
        setattr(candi, 'rating', rating)
    
    fav = max(candidates, key=lambda candi: candi.rating)
    return render(request, 'approval.html', full_context(fav=fav, candidates=candidates))

@login_required(redirect_field_name=None)
def saverange(request):
    record_ratings(request)

    return redirect("/?saved")

def about(request):
    return render(request, 'about.html', full_context())

def npos(request):
    return render(request, 'npos.html', full_context())

def platform(request):
    return render(request, 'platform.html', full_context())

def regions(request):
    return render(request, 'regions.html', full_context())

def blog(request):
    return render(request, 'blog.html', full_context())

def almanac(request):
    return render(request, 'almanac.html', full_context(almanacs = almanacs()))

def get_user_settings(request):
    return UserSettings.objects.get_or_create(user=request.user, defaults=dict(delegate=request.user))

@login_required(redirect_field_name=None)
def account(request):
    settings,created = get_user_settings(request)

    if 'location' in request.POST and request.POST['location'].isalnum():
        settings.location = request.POST['location']
        settings.save()

    if 'handle' in request.POST and request.POST['handle'].isalnum():
        settings.handle = request.POST['handle']
        settings.save()

    return render(request, 'account.html', full_context(settings=settings))

def delegate(request, handle):
    rep = UserSettings.objects.get(handle=handle).user

    if not request.user.is_authenticated():
        return render(request, 'login.html', full_context(delegate=rep, msg='register'))

    settings,created = get_user_settings(request)

    if created:
        settings.delegate = rep
        settings.save()
        return account(request)

    if 'location' in request.POST and request.POST['location'].isalnum():
        settings.location = request.POST['location']
        settings.save()
        return redirect('/vote')
        
    if settings.delegate == rep: #Reusing a delegacy link after completing setup
        return redirect('/')

    if 'confirm' in request.POST:
        settings.delegate = rep
        settings.save()
        return redirect('/account')

    return render(request, 'account.html', full_context(settings=settings, new_delegate=rep))
