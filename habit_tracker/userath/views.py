from django.shortcuts import render
import random, logging
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.shortcuts import redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .forms import ExtendedUserCreationForm

logging.basicConfig(format='%(asctime)s %(levelname)-8s[%(filename)s:%(lineno)d] %(message)s', datefmt='%d-%m-%Y '
                                                                                                       '%H:%M:%S ',
                    level=logging.INFO,
                    filename='logs.txt')
logger = logging.getLogger('userathlogs')


def home(request):
    from functions import encode

    return render(request, 'userath/home.html', {'id': encode(12)})


def sign_up(request):
    from functions import encode
    if request.method == "POST":
        form = ExtendedUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user_id = user.id
            encoded_id = encode(user_id)
            login(request, user)
            return redirect(f'/user_home/{encoded_id}')
    else:
        form = ExtendedUserCreationForm()
    return render(request, 'registration/register.html', {"form": form})


def login_view(request):
    from functions import encode
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        logger.info(user)
        if user is not None:
            encoded_id = encode(user.id)
            login(request, user)
            return redirect(f'/user_home_page/{encoded_id}')
        else:
            error_message = 'Invalid username or password.'
            return render(request, 'registration/login.html',
                          {'error_message': error_message, 'form': AuthenticationForm})

    else:
        # Display the login form
        return render(request, 'registration/login.html', {'form': AuthenticationForm})

# Create your views here.
