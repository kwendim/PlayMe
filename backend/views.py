from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from backend.forms import SignUpForm,GameUploadForm
from .models import Game,Profile
from django.template import RequestContext, loader
from django.contrib.auth.models import User
from django.conf import settings


# Create your views here

@login_required(login_url='login')
def home(request):
    games = Game.objects.all()
    print(settings.MEDIA_URL)
    return render(request, 'home.html', {'games': games, 'MEDIA_URL': settings.MEDIA_URL})

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()  # load the profile instance created by the signal
            user.profile.is_developer = form.cleaned_data.get('is_developer')
            user.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})

@login_required
def upload(request):
	upload_done = False
	if request.method == 'POST':
		form = GameUploadForm(request.POST)
		if form.is_valid():
			uploader  = Profile.objects.get(user = request.user)
			new_game = form.save(commit=False)
			new_game.developer = uploader
			if 'thumbnail' in request.FILES:
				new_game.thumbnail = request.FILES['thumbnail']
			new_game.save()
			upload_done = True
			print(upload_done)
		else:
			print(form.errors)
	else:
		form = GameUploadForm()

	return render(request, 'upload.html',{'form': form, 'MEDIA_URL': settings.MEDIA_URL,  'upload_done':upload_done})


def buy(request,game_id):

	MEDIA_URL = '/media/'
	print(game_id)
	game = Game.objects.get(id = game_id)
	purchase_number = game.number_of_purchases
	return render(request,'buy.html',{'MEDIA_URL' : MEDIA_URL,'game':game	, 'purchase_number': purchase_number})

def aboutus(request):
    return render(request, 'aboutus.html')

def leaderboard(request):
    MEDIA_URL = '/media/'
    games = Game.objects.all()
    return render(request, 'leaderboard.html',{'MEDIA_URL' : MEDIA_URL,'games': games})

def dashboard(request):
    MEDIA_URL = '/media/'
    games = Game.objects.all()
    return render(request, 'dashboard.html',{'MEDIA_URL' : MEDIA_URL,'games': games})
