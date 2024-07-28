from django.shortcuts import render
from django.http import HttpResponseRedirect

from django.contrib import auth
from django.contrib.auth.models import User
from .models import Chat

from django.utils import timezone

def index(request):
    context = {}
    return HttpResponseRedirect('/login')

def chatbot(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/login')
    
    chats = Chat.objects.filter(user=request.user)
    
    if request.method == 'POST':
        # checks if cookies are active
        if request.session.test_cookie_worked():
            message = request.POST.get('prompt')
            
            # get response 
            response = 'this is a response'

            chat = Chat(
                user=request.user, 
                message=message, 
                response=response, 
                created_at=timezone.now(),
            )
            chat.save()
            request.session.delete_test_cookie()
        
    request.session.set_test_cookie()
    return render(request, 'chatbot.html', {'chats': chats})

def login(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/chatbot')
    
    context = {}
    if request.method == 'POST':
        # checks user credentials
        user = auth.authenticate(request, 
            username=request.POST.get('email').strip(), 
            password=request.POST.get('password', False),
        )
        
        if user is not None:
            auth.login(request, user)
            return HttpResponseRedirect('/chatbot')
        else:
            context = {'error_message': 'Correo o contraseña incorrectos.'}
    
    return render(request, 'signindup.html', context)

def register(request):
    context = {}
    if request.method == 'POST':
        # check if passwords match
        if request.POST['password'] == request.POST['password2']:
            # check if email is in use, if not add user to db and redirect to signin
            try:
                user = User.objects.create_user(
                    request.POST.get('email').strip(), 
                    request.POST.get('email').strip(), 
                    request.POST.get('password'), 
                )
                user.save()
                return HttpResponseRedirect('/login')
            except Exception as e:
                print(e)
                context = {'error_message': 'Se ha producido un error.'}
        else:
            context = {'error_message': 'Las contraseñas no coinciden.'}
    
    return render(request, 'signupdup.html', context)

def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/login')