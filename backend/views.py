from django.shortcuts import render, redirect
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from backend.forms import SignUpForm, GameUploadForm
from backend.tokens import account_activation_token
from .models import Game,Profile,Transaction, Score, State
from django.template import RequestContext, loader
from django.contrib.auth.models import User
from django.conf import settings
from hashlib import md5
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.utils import timezone
import json

NUM_OF_SCORES = 3
# Create your views here

def home(request):
    games = Game.objects.all()
    print(settings.MEDIA_URL)
    return render(request, 'home.html', {'games': games, 'MEDIA_URL': settings.MEDIA_URL})

def signup(request):
	if request.user.is_authenticated:
		games = Game.objects.all()
		return redirect('/', {'games': games, 'MEDIA_URL': settings.MEDIA_URL})
	if request.method == 'POST':
		form = SignUpForm(request.POST)
		if form.is_valid():
			user = form.save()
			user.refresh_from_db()
			user.is_active = False
			user.profile.is_developer = form.cleaned_data.get('is_developer')
			user.save()
			current_site = get_current_site(request)
			encodeded_uid = urlsafe_base64_encode(force_bytes(user.pk))
			subject = 'Activate Your PlayMe Account'
			message = render_to_string('account_activation_email.html', {
				'user': user,
				'domain': current_site.domain,
				'uid': encodeded_uid.decode('utf-8'),
				'token': account_activation_token.make_token(user),
			})
			user.email_user(subject, message)
			return redirect('account_activation_sent')
	else:
		form = SignUpForm()
	return render(request, 'registration/signup.html', {'form': form})

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.profile.email_confirmed = True
        user.save()
        login(request, user)
        games = Game.objects.all()
        return redirect('/', {'games': games, 'MEDIA_URL': settings.MEDIA_URL})
    else:
        return render(request, 'account_activation_invalid.html')

def account_activation_sent(request):
	return render(request, 'account_activation_sent.html')

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
def delete_upload(request):
	game_id = request.GET['id']
	game = Game.objects.get(id = game_id)

	if request.method == 'POST':
		game.delete()
		print('game deleted')
		return redirect('developer_uploads')
	else:
		return render(request, 'confirm_delete.html', {'game':game})


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

	game = Game.objects.get(id = game_id)
	check_if_bought = Transaction.objects.filter(payer = request.user.profile,game__id=game_id,state=Transaction.CONFIRMED).count()
	if check_if_bought == 0 and request.user.profile != game.developer:
		games = Game.objects.all()
		return render(request, 'home.html', {'games': games, 'MEDIA_URL': settings.MEDIA_URL})
	
	high_scores = Score.objects.filter(game__id=game_id).prefetch_related('player__user__username').order_by('-current_score').values('player__user__username', 'current_score').distinct()
	player_scores = Score.objects.filter(game__id=game_id, player__user=request.user).order_by('-current_score').values('current_score').distinct()
	if len(high_scores) > NUM_OF_SCORES:
		high_scores = high_scores[:NUM_OF_SCORES]
	if len(player_scores) > NUM_OF_SCORES:
		player_scores = player_scores[:NUM_OF_SCORES]
	
	
	return render(request,'play.html',{'MEDIA_URL' : MEDIA_URL,'game':game, 'player_scores':player_scores, 'high_scores':high_scores})


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

@csrf_exempt
def submit_score(request, game_id):
	try:
		game = Game.objects.get(id=game_id)
		profile = Profile.objects.get(user=request.user)
		new_score = float(request.POST['score'])
		score = Score(game=game, player=profile, current_score=new_score)
		score.save()
		return JsonResponse(data={'status':'Score submitted successfully!'})
	except Exception as e:
		return JsonResponse(data={}, status=500)

@login_required(login_url='login')
def developer_uploads(request):
	games = Game.objects.filter(developer = request.user.profile)
	print(games)
	return render(request,'developer_uploads.html',{'games': games, 'MEDIA_URL': settings.MEDIA_URL})
@csrf_exempt
def save_game(request, game_id):
	try:
		game = Game.objects.get(id=game_id)
		profile = Profile.objects.get(user=request.user)
		new_state = json.dumps(json.loads(request.body))
		State.objects.update_or_create(
        game=game, player=profile, 
		defaults={"game": game, "player": profile, "current_state": new_state})
		return JsonResponse({'status':'Game saved successfully!'})
	except Exception as e:
		return JsonResponse(data={}, status=500)

def aboutus(request):
    return render(request, 'aboutus.html')

def leaderboard(request):
    MEDIA_URL = '/media/'
    games = Game.objects.all()
    return render(request, 'leaderboard.html',{'MEDIA_URL' : MEDIA_URL,'games': games})

@login_required(login_url='login')
def developer_dahsboard(request):
	games = Game.objects.filter(developer = request.user.profile)
	return render(request, "dashboard.html", {'MEDIA_URL': settings.MEDIA_URL, 'games': games})
@csrf_exempt
def load_game(request, game_id):
	try:
		state = State.objects.filter(game__id=game_id, player__user=request.user).first()
		return JsonResponse(state.current_state, safe=False)
	except Exception as e:
		return JsonResponse(data={}, status=500)