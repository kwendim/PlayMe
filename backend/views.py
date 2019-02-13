from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from backend.forms import SignUpForm,GameUploadForm
from .models import Game,Profile,Transaction
from django.template import RequestContext, loader
from django.contrib.auth.models import User
from django.conf import settings
from hashlib import md5

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
	return render(request,'buy.html',{'MEDIA_URL' : MEDIA_URL,'game':game, 'purchase_number': purchase_number})


def payment(request,game_id):
	purchase_game = Game.objects.get(id = game_id)
	new_payer = Profile.objects.get(user = request.user)	
	new_payee=  purchase_game.developer
	transaction = Transaction.objects.create(payer=new_payer, payee= new_payee, game=purchase_game,amount=purchase_game.price)
	transaction.save()
	checksumstr = "pid={}&sid={}&amount={}&token={}".format(transaction.id, settings.SELLER_ID, purchase_game.price, settings.SELLER_KEY)
	m = md5(checksumstr.encode("ascii"))
	checksum =   m.hexdigest() 
	print(transaction.id, transaction.state, checksumstr)
	return render(request, 'payment.html', {'game':purchase_game,'SELLER_ID':settings.SELLER_ID, 'MEDIA_URL': settings.MEDIA_URL, 'transaction': transaction, 'checksum': checksum})

def payment_success(request):
	secret_key = settings.SELLER_KEY
	pid = request.GET['pid']
	ref = request.GET['ref']
	result = request.GET['result']
	checksumstr = "pid={}&ref={}&result={}&token={}".format(pid, ref, result, secret_key)
	m = md5(checksumstr.encode("ascii"))
	checksum = m.hexdigest()
	malformed = False
	print("calculated: " + checksum)
	print("received: " + request.GET['checksum'] )
	if (checksum == request.GET['checksum'] ):			
		transaction = Transaction.objects.get(pk=pid)
		transaction.state = Transaction.CONFIRMED
		transaction.reference = ref
		game = transaction.game
		transaction.save()
		print("about to call success")
		return render(request, 'success.html', {'game': game, 'MEDIA_URL': settings.MEDIA_URL, 'malformed': malformed})
	else: 
		transaction = Transaction.objects.get(pk=pid)
		transaction.delete()
		malformed = True
		return render(request, 'success.html', {"malformed": malformed})
		

def payment_cancel(request):
	transaction = Transaction.objects.get(pk=request.GET['pid'])
	game = transaction.game
	transaction.delete()
	print("about to call redirect")
	return redirect('/' + str(game.id))

def payment_error(request):
	try:
		transaction = Transaction.objects.get(pk=request.GET['pid'])
		game = transaction.game
		transaction.delete()
		return render(request, 'error.html')

	except:
		return render(request, 'error.html')



