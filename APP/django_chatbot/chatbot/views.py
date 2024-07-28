from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect

from django.contrib import auth
from django.contrib.auth.models import User
from .models import Chat, UserChatList

from django.utils import timezone

import requests

USERCHAT_LIST = None

def get_response(context):
    response = requests.post("https://c454-181-63-26-23.ngrok-free.app/ask", json=context)
    return response.json()['response']

def index(request):
    return HttpResponseRedirect('/login')

def newchat(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/login')
    else: 
        try:
            if USERCHAT_LIST != None:
                pass
        except:
            USERCHAT_LIST = UserChatList.objects.filter(user=request.user)
    
    userchat = UserChatList(
        user=request.user,
        title='Nuevo Chat',
        created_at=timezone.now(),
    )
    userchat.save()
    
    USERCHAT_LIST = UserChatList.objects.filter(user=request.user)
    
    return HttpResponseRedirect(f'{userchat.id}/chatbot')

def chatbot_delete(request, userchat_id):
    if not request.user.is_authenticated:
        # if user is not logged in
        return HttpResponseRedirect('/login')
    else: 
        # else fetches user chat list
        try:
            if USERCHAT_LIST != None:
                pass
        except:
            USERCHAT_LIST = UserChatList.objects.filter(user=request.user)
    
    # checks if current chat is in user chat list
    try:
        # if it is, carries out deletion and redirects to a previous chat
        current_chat = USERCHAT_LIST.get(pk=userchat_id)
        current_chat.delete()
        
        USERCHAT_LIST = UserChatList.objects.filter(user=request.user)
    except:
        pass
    
    return HttpResponseRedirect(f'/{[c for c in USERCHAT_LIST][-1].id}/chatbot')

def chatbot_edit(request, url_id):
    
    if not request.user.is_authenticated:
        # if user is not logged in
        return HttpResponseRedirect('/login')
    else: 
        
        # else fetches user chat list
        try:
            if USERCHAT_LIST != None:
                pass
        except:
            USERCHAT_LIST = UserChatList.objects.filter(user=request.user)
    
    # checks if current chat is in user chat list
    try:
        # if it is, fetches current chat info
        current_chat = USERCHAT_LIST.get(pk=url_id)
    except Exception as e:
        # else, redirects to last chat
        return HttpResponseRedirect(f'/{[c for c in USERCHAT_LIST][-1].id}/chatbot')
    
    if request.method == 'POST':
        # changes title and redirects to chat
        current_chat.title = request.POST.get('title-input').strip()
        current_chat.save()
        
        USERCHAT_LIST = UserChatList.objects.filter(user=request.user)
        
        return HttpResponseRedirect(f'/{current_chat.id}/chatbot')
        
    return render(
        request, 
        'chatbot-edit.html', 
        {'userchat': current_chat,
         'userchat_list': USERCHAT_LIST},
    )

def chatbot(request, userchat_id):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/login')
    else: 
        try:
            if USERCHAT_LIST != None:
                pass
        except:
            USERCHAT_LIST = UserChatList.objects.filter(user=request.user)
    
    try:
        current_chat = USERCHAT_LIST.get(pk=userchat_id)
    except: # chat does not exist; redirects to last chat
        return HttpResponseRedirect(f'/{[c for c in USERCHAT_LIST][-1].id}/chatbot')
    
    chats = [c for c in Chat.objects.filter(userchat_macro=current_chat)]
    
    if request.method == 'POST':
        message = request.POST.get('prompt')
        
        fc = timezone.now()
        
        history = [{"role": c.role, "content": c.content} for c in chats]
        # get response 
        # TODO: REVISAR SI MANDAR HISTORIAL; LA SIGUIENTE ES LA LÍNEA QUE GENERA LA RESPUESTA
        response = get_response({"content": message, "history": []})
        
        chat = Chat(
            user=request.user, 
            role="user", 
            content=message, 
            created_at=fc,
            userchat_macro=current_chat,
        )
        chat.save()
        chats.append(chat)
        
        chat = Chat(
            user=request.user, 
            role="assistant", 
            content=response, 
            created_at=timezone.now(),
            userchat_macro=current_chat,
        )
        chat.save()
        chats.append(chat)
    
    return render(
        request, 
        'chatbot.html', 
        {'chats': chats, 'userchat': current_chat, 'userchat_list': USERCHAT_LIST},
    )

def login(request):
    if request.user.is_authenticated:
        try:
            if USERCHAT_LIST != None:
                pass
        except:
            USERCHAT_LIST = UserChatList.objects.filter(user=request.user)
            if len(USERCHAT_LIST) == 0:
                return HttpResponseRedirect('/newchat')
            else:
                return HttpResponseRedirect(f'{[c for c in USERCHAT_LIST][-1].id}/chatbot')
    
    context = {}
    if request.method == 'POST':
        # checks user credentials
        user = auth.authenticate(request, 
            username=request.POST.get('email').strip(), 
            password=request.POST.get('password', False),
        )
        
        if user is not None:
            auth.login(request, user)
            USERCHAT_LIST = UserChatList.objects.filter(user=request.user)
            if len(USERCHAT_LIST) == 0:
                return HttpResponseRedirect('/newchat')
            else:
                return HttpResponseRedirect(f'{[c for c in USERCHAT_LIST][-1].id}/chatbot')
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
                context = {'error_message': 'Se ha producido un error.'}
        else:
            context = {'error_message': 'Las contraseñas no coinciden.'}
    
    return render(request, 'signupdup.html', context)

def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/login')