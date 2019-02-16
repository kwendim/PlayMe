from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from backend.forms import SignUpForm,GameUploadForm
from .models import Game,Profile,Transaction
from django.template import RequestContext, loader
from django.contrib.auth.models import User
from django.conf import settings
from hashlib import md5
from django.shortcuts import get_object_or_404


# Create your views here

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
        form = SignUpForm(initial={'last_name': 'hello'})
    return render(request, 'registration/signup.html', {'form': form})

@login_required(login_url='login')
def mygames(request):
	transactions = Transaction.objects.filter(
		payer__user=request.user,
		state=Transaction.CONFIRMED
	).select_related('game')
	
	return render(request, 'mygames.html', {'transactions': transactions, 'MEDIA_URL': settings.MEDIA_URL})

@login_required(login_url='login')
def upload(request):
	if (request.user.profile.is_developer): #checks if a developer is accessing the upload page
		upload_done = False
		if request.method == 'POST':
			form = GameUploadForm(request.POST, request.FILES)
			if form.is_valid():
				uploader  = request.user.profile	
				new_game = form.save(commit=False)
				new_game.developer = uploader
				new_game.save()
				upload_done = True
			else:
				print(form.errors)
		else:		
			form = GameUploadForm()	
			is_edit = False		
		
			
		return render(request, 'upload.html',{'form': form, 'MEDIA_URL': settings.MEDIA_URL,
		  'upload_done':upload_done})

	else:
		return redirect('home')

@login_required(login_url='login')
def edit_upload(request):
	game_edit_id = request.GET.get('id') 
	upload_done = False
	if request.method == 'POST':
		the_game = get_object_or_404(Game,id = game_edit_id)
		form = GameUploadForm(request.POST, request.FILES, instance = the_game )
		print(form)
		if form.is_valid():
			form.save()
			upload_done = True
		else:
			print(form.errors)
	else:
		game_exits = Game.objects.filter(id= game_edit_id).count()
		if (game_exits > 0):
			game = Game.objects.get(id = game_edit_id)
			form = GameUploadForm(initial = {'name': game.name, 'category': game.category,
				'description': game.description, 'link':game.link, 'price': game.price})
			print("hello from edit")
			is_edit=True
		else: 
			return redirect('home')
	
	is_edit = True
	return render(request, 'upload.html',{'form': form, 'MEDIA_URL': settings.MEDIA_URL,
		  'upload_done':upload_done, 'is_edit': 'is_edit', "game_id": game_edit_id})


@login_required(login_url='login')
def buy(request,game_id):	 
	MEDIA_URL = '/media/'
	print(game_id)
	game = Game.objects.get(id = game_id)
	user_has_bought_game = False
	check_if_bought = Transaction.objects.filter(payer = request.user.profile,game=game,state=Transaction.CONFIRMED).count() #check if user has already purchased the game
	is_developers_game = False
	if (check_if_bought > 0):
		user_has_bought_game = True
	if (request.user.profile == game.developer):
			is_developers_game = True

	return render(request,'buy.html',{'MEDIA_URL' : MEDIA_URL,'game':game, 'user_has_bought_game': user_has_bought_game, 'is_developers_game':is_developers_game})

@login_required(login_url='login')
def play(request,game_id):	 
	MEDIA_URL = '/media/'
	print(game_id)
	game = Game.objects.get(id = game_id)
	return render(request,'play.html',{'MEDIA_URL' : MEDIA_URL,'game':game})


@login_required(login_url='login')
def payment(request,game_id):
	game = Game.objects.filter(id = game_id)
	if(game.count() >  0): #check if the game exists
		check_if_bought = Transaction.objects.filter(payer = request.user.profile,game=Game.objects.get(id=game_id),state=Transaction.CONFIRMED).count() #check if user has already purchased the game
		if (check_if_bought):
			return redirect("/play/" + str(game_id))
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
	else:
		return redirect('home')

@login_required(login_url='login')
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
		
@login_required(login_url='login')
def payment_cancel(request):
	transaction = Transaction.objects.get(pk=request.GET['pid'])
	game = transaction.game
	transaction.delete()
	print("about to call redirect")
	return redirect('/' + str(game.id))

@login_required(login_url='login')
def payment_error(request):
	try:
		transaction = Transaction.objects.get(pk=request.GET['pid'])
		game = transaction.game
		transaction.delete()
		return render(request, 'error.html')

	except:
		return render(request, 'error.html')


login_required(login_url='login')
def developer_uploads(request):
	games = Game.objects.filter(developer = request.user.profile)
	print(games)
	return render(request,'developer.html',{'games': games, 'MEDIA_URL': settings.MEDIA_URL})
