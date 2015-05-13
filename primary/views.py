from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.templatetags.static import static

from datetime import datetime

from django.contrib.auth.models import User
from models import Region, Candidate, Approval, UserSettings, Affiliation, Sums, Weight

def sections():
    return [{'title': 'Primary', 'location': '/'},
            {'title': 'Platform', 'location': '/platform'},
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

def myrender(request, template, **kwargs):
    return render(request, template,
                  dict({'absolute_uri': request.build_absolute_uri(),
                        'absolute_banner_uri': request.build_absolute_uri(static('ddp-square-og.png')),
                        'sections': sections(),
                        'is_party': False,
                        'regions': Region.objects.all()},
                       **kwargs))

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

def get_region(request):
    if request.user.is_authenticated():
        settings,created = get_user_settings(request)
        return settings.region

    return Region.objects.get(id=5)

def get_percentages(request):
    ratings = Sums.objects.filter(candidate__region=get_region(request))
    total = max(sum(map(lambda r: r.approval, ratings)), 1)
    for rating in ratings:
        rating.approval = 100 * rating.approval / total

        # arbitrary scaling factor and minimum width
        setattr(rating, 'display_width', min(25, max(2, rating.approval)) * 22)

    return sorted(ratings, key=lambda rating: rating.candidate.shame, reverse=True)

def get_ballot(request):
    percentages = get_percentages(request)
    return sorted(map(lambda rating: rating.candidate,
                      sorted(percentages, key=lambda rating: rating.approval, reverse=True)),
                  key=lambda candidate: candidate.shame)

def user_voted(request):
    return Approval.objects.filter(user=request.user, candidate__region=get_region(request)).count() > 0

def primary(request):
    return myrender(request, 'primary.html', 
                    ratings = get_percentages(request),
                    # .distinct unavailable on sqlite3, which is used for testing
                    numvotes = Approval.objects.filter(candidate__region=get_region(request)).values('user').annotate(Count('user')).count(),
                    voted = request.user.is_authenticated() and user_voted(request),
                    saved = ('saved' in request.GET))

def vote(request, region="usapres"):
    if not request.user.is_authenticated():
        return myrender(request, 'login.html', msg = 'vote')

    settings,created = get_user_settings(request)
    if created:
        settings.region = Region.objects.get(url=region)
        settings.save()

    if not user_voted(request) and 'fav' not in request.POST:
        return myrender(request, 'vote.html', candidates = get_ballot(request))

    if 'fav' in request.POST:
        for approval in Approval.objects.filter(user=request.user, candidate__region=get_region(request)):
            if approval.rating == 10:
                approval.rating = 9
                approval.save()

        record_one_rating(request, int(request.POST['fav']), 10)

    candidates = get_ballot(request)
    for candi in candidates:
        rating = 0
        try:
            rating = Approval.objects.get(candidate=candi, user=request.user).rating
        except Approval.DoesNotExist:
            pass
        setattr(candi, 'rating', rating)
    
    fav = max(candidates, key=lambda candi: candi.rating)
    return myrender(request, 'approval.html', fav=fav, candidates=candidates)

@login_required(redirect_field_name=None)
def saverange(request):
    record_ratings(request)

    return redirect("/?saved")

def about(request):
    return myrender(request, 'about.html')

def npos(request):
    return myrender(request, 'npos.html')

def platform(request):
    return myrender(request, 'platform.html')

def regions(request):
    return myrender(request, 'regions.html')

def blog(request):
    return myrender(request, 'blog.html')

def almanac(request):
    return myrender(request, 'almanac.html', almanacs = almanacs())

def release(request):
    return myrender(request, 'release.html')

def closewindow(request):
    return myrender(request, 'closewindow.html')

def get_user_settings(request):
    usapres = Region.objects.get(id=5)
    return UserSettings.objects.get_or_create(user=request.user, defaults=dict(delegate=request.user, region=usapres))

def placard(acct):
    return render_to_string('placard.html', {'acct':acct})

def delegate_details(settings):
    return render_to_string('delegate.html', {'placard':placard(settings.user),
                                              'affiliates':Affiliation.objects.filter(user=settings.user),
                                              'settings':settings})

@login_required(redirect_field_name=None)
def account(request):
    settings,created = get_user_settings(request)

    if 'location' in request.POST and request.POST['location'].isalnum():
        settings.location = request.POST['location']
        settings.save()

    if 'region' in request.POST:
        settings.region = Region.objects.get(id=int(request.POST['region']))
        settings.save()
    
    if 'handle' in request.POST and request.POST['handle'].isalnum():
        if UserSettings.objects.filter(handle=request.POST['handle']).count() == 0:
            settings.handle = request.POST['handle']
            settings.save()

    constituency_size = 0
    try:
        constituency_size = Weight.objects.get(user=request.user).count
    except Weight.DoesNotExist:
        pass

    return myrender(request, 'account.html',
                    settings=settings,
                    constituency_size=constituency_size,
                    user_placard=placard(request.user),
                    delegate_placard=placard(settings.delegate))

def delegate(request, handle):
    delegate_settings = UserSettings.objects.get(handle=handle)
    rep = delegate_settings.user

    if not request.user.is_authenticated():
        return myrender(request, 'login.html', msg='register',
                        delegate_details=delegate_details(delegate_settings))

    settings,created = get_user_settings(request)

    if created:
        settings.delegate = rep
        settings.region = UserSettings.objects.get(user=rep).region
        settings.save()
        return account(request)

    if 'location' in request.POST and request.POST['location'].isalnum():
        settings.location = request.POST['location']
        settings.save()
        return redirect('/vote')

    if settings.delegate == rep:
        return myrender(request, 'anything.html', anything=delegate_details(delegate_settings))

    if 'confirm' in request.POST:
        settings.delegate = rep
        settings.save()
        return redirect('/account')

    return myrender(request, 'account.html', settings=settings,
                    new_delegate=delegate_details(delegate_settings))
