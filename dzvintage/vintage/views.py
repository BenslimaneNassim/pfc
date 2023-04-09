from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from .models import *
from django.conf import settings
from django.utils import timezone
from django.core.mail import send_mail
from django.db.models import Q
#from .forms import CommandeForm 
import json
import urllib
#from .helpers import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse
from django.views import View


# Create your views here.
from django.views.generic import RedirectView, View
from django.urls import reverse_lazy
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from allauth.socialaccount.providers.oauth2.views import (OAuth2CallbackView, OAuth2LoginView)
from allauth.socialaccount.models import SocialAccount




def index(request):
    categories = Category.objects.all()
    products = Post.objects.all()
    posts = []
    for i in range(1, 9):
        posts.append(products[0])
    new_products = Post.objects.all().order_by('-created_at')
    new_posts = []
    for i in range(1, 5):
        new_p = new_products[0]
        new_posts.append(new_p)
    context = {'categories':categories, 'products':posts, 'new_products':new_posts}
    if request.user.is_authenticated:
        user = request.user
        profile = Profile.objects.get(user=user)
        context.update({'profile':profile})

    return render(request, 'vintage/index.html', context)
def search(request):
    context = {}
    if request.method == "POST":
        if request.POST.get('search'):
            searched = request.POST.get('search')
            categories = Category.objects.filter(name__contains=searched)
            products1=[]
            for cat in categories:
                prs = Post.objects.filter(category=cat)
                for pr in prs:
                    if pr not in products1:
                        products1.append(pr)
            
            products2 = Post.objects.filter(Q(name__contains=searched) | Q(types__contains=searched))# | Q(design=designs)
            products=[]
            for pr in products1:
                products.append(pr)
            for pr in products2:
                if pr not in products:
                    products.append(pr)
            context['products'] = products
            context['searched'] = searched

    return render(request,"vintage/search.html",context)


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('/')
    else:
        form = UserCreationForm()
    return render(request, 'vintage/signup.html', {'form': form})

def post(request, genre, category, product_name):
    context = {}
    category = Category.objects.get(name=category)
    product = Post.objects.get(title=product_name, genre= genre, category= category)
    images = PostPicture.objects.filter(post=product)
    context.update({'product':product,'images':images})

    return render(request,"vintage/post.html",context)

@login_required(login_url='/login/')
def chat(request, other_user, product_id):
    context = {}
    user = request.user
    if product_id != 'inbox' and other_user != 'inbox':
        other_user = User.objects.get(username=other_user)
    profile = Profile.objects.get(user=user)

    if request.method == "POST":
        if request.POST.get('message'):
            message = request.POST.get('message')
            post = Post.objects.get(id=product_id)
            # if post.seller == user:
            #     receiver = post.buyer
            # else:
            #     receiver = post.seller
            chat = Chat.objects.create(sender=user, receiver=other_user , post=post, message=message)
            chat.save()
            return redirect('/chat/'+other_user.username+'/'+product_id)

    all_chats = Chat.objects.filter(Q(sender=user) | Q(receiver=user)).order_by('-timestamp')
    conversations = []
    temps = []
    for chat in all_chats:
        if chat.sender == user:
            other_userr = chat.receiver
        else:
            other_userr = chat.sender

        conversation = {
            'post': chat.post,
            'other_user': other_userr,
            'last_message': chat.message,
            'timestamp': chat.timestamp,
        }
        temp = {
            'post': chat.post,
            'other_user': other_userr,
        }
        if temp not in temps:
            temps.append(temp)
            conversations.append(conversation)

    context.update({'conversations':conversations})

    if product_id == "inbox" or other_user == "inbox":
        pass
    else:
        product = Post.objects.get(id=product_id)
        messages = Chat.objects.filter( Q(Q(sender=user) & Q(receiver=other_user)) | Q(Q(sender=other_user) & Q(receiver=user)) , post=product).order_by('timestamp')
        context.update({'product':product, 'other_user': other_user, 'messages':messages})


    context.update({'profile':profile})
    return render(request,"vintage/chat.html",context)

def category(request, genre, category):
    context = {}
    if category != "all":
        category = Category.objects.get(name=category)
        products = Post.objects.filter(category=category, genre=genre)
    else:
        products = Post.objects.filter(genre=genre)
    context.update({'products':products,'category':category,'genre':genre})
    return render(request,"vintage/category.html",context)
def customnotfound(request, exception):
    context = {}
    return render(request, "vintage/404.html",context)
def customserver(request):
    context = {}
    return render(request, "vintage/500.html",context)