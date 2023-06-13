from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from .models import *
from .helpers import *
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
from django.views.decorators.csrf import csrf_exempt
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


from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView
from django.db.models import Max
def index(request):
    # send_mail(
    #     'Test_smtp','amek dina',settings.EMAIL_HOST_USER,['nassimbenslimane123@gmail.com'], fail_silently=False
    # )

    context = {}
    context = categories(request, context)
    products = Post.objects.filter(deleted=False).order_by('-nb_likes')
    new_products = Post.objects.filter(deleted=False).order_by('-created_at')
    posts = []
    for pr in products:
        posts.append(pr)
    # for i in range(1, 6):
    #     posts.append(products[0])

    new_posts = []
    for pr in new_products:
        new_posts.append(pr)
    if request.user.is_authenticated:
        user = request.user
        followed_users = User.objects.filter(followed__follower=user)
        posts_followed = Post.objects.filter(seller__in=followed_users, deleted=False).order_by('-created_at')[:8]

    context.update({'products':posts, 'new_products':new_posts})

    if request.user.is_authenticated:
        user = request.user
        profile = Profile.objects.get(user=user)
        liked = Article_Like.objects.filter(user=user)
        print(liked)
        likedd = []
        for like in liked:
            likedd.append(like.post)
        for post in posts:
            if post in likedd:
                post.liked = True
        for post in posts_followed:
            if post in likedd:
                post.liked = True
        for post in new_posts:
            if post in likedd:
                post.liked = True
        context.update({'profile':profile, 'products':posts, 'new_products':new_posts, 'followed_products':posts_followed})


    return render(request, 'vintage/index.html', context)

from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

@csrf_exempt
def telegram_webhook(request):
    if request.method == 'POST':
        async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        # commands = ['/start', '/help']
        # if update.message.text not in commands:
        #     await update.message.reply_text(f'Commande inconnue {update.effective_user.first_name} \n Appuyez sur /help pour plus d\'informations')
        # else:
            await update.message.reply_text(f'Bienvenue sur VintagedZ {update.effective_user.first_name} \n Appuyez sur /help pour plus d\'informations')



        async def help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
            await update.message.reply_text('Je suis là pour vous aider')


        app = ApplicationBuilder().token(settings.TELEGRAM_BOT_TOKEN).build()

        app.add_handler(CommandHandler("start", start))
        app.add_handler(CommandHandler("help", help))

        app.run_polling()
    return HttpResponse()


def products(request, cat):
    context = {}
    context = categories(request, context)
    if cat == "tout":
        products = Post.objects.filter(deleted=False)
    else:
        cat = Category.objects.get(name=cat)
        products = Post.objects.filter(category=cat, deleted=False)
        context.update({'cat':cat})
    if request.user.is_authenticated:
        user = request.user
        liked = Article_Like.objects.filter(user=user)
        likedd = []
        for like in liked:
            likedd.append(like.post)
        for post in products:
            if post in likedd:
                post.liked = True
    posts = []
    for pr in products:
        try:
            # for i in range(1, 6):
            posts.append(pr)
        except:
            context.update({'nothing':'nothing'})
    context.update({'products':posts})
    return render(request, 'vintage/products.html', context)
@login_required
def profile(request):
    context = {}
    context = categories(request, context)
    profile = Profile.objects.get(user=request.user)
    context.update({'profile':profile,'wilayas':WILAYAS})

    if request.method == "POST":
        print("pre-ok")
        if request.FILES.get('picture'):
            picture = request.FILES.get('picture')
            profile.picture = picture
            profile.save()
        if request.POST.get('bio'):
            if request.POST.get('bio') == profile.bio:
                pass
            else:
                bio = request.POST.get('bio')
                profile.bio = bio
                profile.save()
        if request.POST.get('wilaya'):
            wilaya = request.POST.get('wilaya')
            if wilaya == profile.wilaya:
                pass
            else:
                profile.wilaya = wilaya
                profile.save()
        if request.POST.get('phone_number'):
            phone_number = request.POST.get('phone_number')
            if phone_number == profile.phone_number:
                pass
            else:
                if Profile.objects.filter(phone_number=phone_number).exists():
                    context.update({'error':'Le numéro de téléphone est déja utilisé'})
                    return render(request, 'vintage/profile.html', context)
                else:
                    profile.phone_number = phone_number
                    profile.save()
        if request.POST.get('first_name'):
            first_name = request.POST.get('first_name')
            if first_name == request.user.first_name:
                pass
            else:
                request.user.first_name = first_name
                request.user.save()
        if request.POST.get('last_name'):
            last_name = request.POST.get('last_name')
            if last_name == request.user.last_name:
                pass
            else:
                request.user.last_name = last_name
                request.user.save()
        if request.POST.get('username'):
            username = request.POST.get('username')
            if username == request.user.username:
                pass
            else:
                if User.objects.filter(username=username).exists():
                    context.update({'error':'Le nom d\'utilisateur est déja utilisé'})
                    return render(request, 'vintage/profile.html', context)
                else:
                    request.user.username = username
                    request.user.save()
        if request.POST.get('email'):
            email = request.POST.get('email')
            if email == request.user.email:
                pass
            else:
                if User.objects.filter(email=email).exists():
                    context.update({'error':'L\'adresse email est déja utilisée'})
                    return render(request, 'vintage/profile.html', context)
                else:
                    request.user.email = email
                    request.user.save()
        return redirect('/profile/')

        
    return render(request, 'vintage/profile.html', context)

@login_required
def annonces(request):
    context = {}
    context = categories(request, context)
    user = request.user
    profile = Profile.objects.get(user=user)
    products = Post.objects.filter(seller=user, deleted=False)
    posts = []
    for pr in products:
        posts.append(pr)
    context.update({'products':products,'profile':profile})
    return render(request, 'vintage/annonces.html', context)

@login_required
def change_panier(request, product_id):
    product = Post.objects.get(id=product_id)
    cart = Article_Panier.objects.filter(user=request.user, post=product)
    if cart.exists():
        cart.delete()
    else:
        Article_Panier.objects.create(user=request.user, post=product)
    return redirect(request.META.get('HTTP_REFERER', '/'))

@login_required
def add(request):
    user = request.user
    profile = Profile.objects.get(user=user)
    context = {}
    context = categories(request, context)
    context.update({'profile':profile,'genres':GENDER})
    if request.method == "POST":
        if request.POST.get('title') and request.POST.get('genre') and request.POST.get('price') and request.POST.get('bio') and request.POST.get('category'):
            title = request.POST.get('title')
            genre = request.POST.get('genre')
            price = request.POST.get('price')
            bio = request.POST.get('bio')
            category = request.POST.get('category')
            category = Category.objects.get(id=category)
            if request.POST.get('taille'):
                taille = request.POST.get('taille')
            else:
                taille = None
            if request.POST.get('discounted_price'):
                discounted_price = request.POST.get('discounted_price')
            else:
                discounted_price = None
            if request.FILES.getlist('pictures'):
                pictures = request.FILES.getlist('pictures')
                image = pictures[0]
                pictures.pop(0)
            post = Post.objects.create(title=title, genre=genre, price=price, description=bio, category=category, seller=user, taille=taille, discounted_price=discounted_price, image=image)
            post.save()
            if pictures:
                for pic in pictures:
                    picture = PostPicture.objects.create(post=post, image=pic)
                    picture.save()



    return render(request, 'vintage/ajouter.html', context)

@login_required
def delete(request, product_id):
    product = Post.objects.get(id=product_id)
    product.deleted = True
    product.save()
    return redirect(request.META.get('HTTP_REFERER', '/'))

@login_required
def modify(request, product_id):
    user = request.user
    product = Post.objects.get(id=product_id)
    profile = Profile.objects.get(user=user)
    images = PostPicture.objects.filter(post=product)
    context = {}
    context = categories(request, context)
    context.update({'profile':profile,'product':product,'images':images, 'genres':GENDER})
    if request.method == 'POST':
        if request.FILES.get('image'):
            image = request.FILES.get('image')
            post_image = PostPicture.objects.create(post=product, image=image)
            post_image.save()
        if request.FILES.get('picture'):
            picture = request.FILES.get('picture')
            product.image = picture
            product.save()
        if request.POST.get('title'):
            title = request.POST.get('title')
            product.title = title
            product.save()
        if request.POST.get('genre'):
            genre = request.POST.get('genre')
            product.genre = genre
            product.save()
        if request.POST.get('price'):
            price = request.POST.get('price')
            product.price = price
            product.save()
        if request.POST.get('bio'):
            bio = request.POST.get('bio')
            product.description = bio
            product.save()
        if request.POST.get('category'):
            category = request.POST.get('category')
            category = Category.objects.get(id=category)
            product.category = category
            product.save()
        if request.POST.get('taille'):
            taille = request.POST.get('taille')
            product.taille = taille
            product.save()
        if request.POST.get('discounted_price'):
            discounted_price = request.POST.get('discounted_price')
            product.discounted_price = discounted_price
            product.save()
        return redirect(request.META.get('HTTP_REFERER', '/'))



    return render(request, 'vintage/modifier.html', context)

@login_required
def delete_pic(request, pic_id):
    pic = PostPicture.objects.get(id=pic_id)
    pic.delete()
    return redirect(request.META.get('HTTP_REFERER', '/'))

@login_required
def likeit(request, product_id):
    user = request.user
    product = Post.objects.get(id=product_id)
    if Article_Like.objects.filter(user=user, post=product).exists():
        Article_Like.objects.filter(user=user, post=product).delete()
    else:
        Article_Like.objects.create(user=user, post=product)
    return redirect(request.META.get('HTTP_REFERER', '/'))

@login_required
def follow(request, username):
    user = request.user
    his_user = User.objects.get(username=username)
    if Abonnement.objects.filter(follower=user, followed=his_user).exists():
        Abonnement.objects.filter(follower=user, followed=his_user).delete()
    else:
        Abonnement.objects.create(follower=user, followed=his_user)
    return redirect(request.META.get('HTTP_REFERER', '/'))

def search(request):
    context = {}
    context = categories(request, context)
    if request.method == "POST":
        products = None
        # min_price = request.POST.get('min')
        # max_price = request.POST.get('max')

        if request.POST.get('search'):
            searched = request.POST.get('search')
            context['searched'] = searched
            categories_searched = Category.objects.filter(name__contains=searched)
            products1 = Post.objects.filter(category__in=categories_searched, deleted=False)
            
            products2 = Post.objects.filter(Q(title__contains=searched) | Q(genre__contains=searched)| Q(description__contains=searched), deleted=False)
            products = (products1 | products2).distinct().order_by('price')
            
        # if request.POST.get('genre'):
        #     genre = request.POST.get('genre')
        #     if products:
        #         products = products.filter(genre=genre)
        #     else:
        #         products = Post.objects.filter(genre=genre, deleted=False)
            
        #     if request.POST.get('min') and request.POST.get('max'):
        #         if products == None:
        #             products = Post.objects.filter(Q( Q(discounted_price = None) & Q(price__range=(min_price,max_price)) ) | Q(discounted_price__range=(min_price,max_price)), deleted=False)
        #         products = products.filter( Q( Q(discounted_price = None) & Q(price__range=(min_price,max_price)) ) | Q(discounted_price__range=(min_price,max_price)), deleted=False )

        # if request.POST.get('min') and request.POST.get('max'):
            # if products:
            #     print(products)
            # else:
            #     products = Post.objects.filter( Q( Q(discounted_price = None) & Q(price__range=(min_price,max_price)) ) | Q(discounted_price__range=(min_price,max_price)) )
        # if request.POST.get('category'):
            
        #     categoryy = request.POST.get('category')
        #     if categoryy != "All":
        #         categoryy = Category.objects.get(name=categoryy)
        #         if products:
        #             # products = products.filter(genre=genre, category=categoryy)
        #             products = products.filter(category=categoryy)
        #         else:
        #             # products = Post.objects.filter(genre=genre, category=categoryy)
        #             products = Post.objects.filter(category=categoryy, deleted=False)
        #     if request.POST.get('min') and request.POST.get('max'):
        #         if products == None:
        #             products = Post.objects.filter(Q( Q(discounted_price = None) & Q(price__range=(min_price,max_price)) ) | Q(discounted_price__range=(min_price,max_price)), deleted=False)

        #         products = products.filter( Q( Q(discounted_price = None) & Q(price__range=(min_price,max_price)) ) | Q(discounted_price__range=(min_price,max_price)), deleted=False )

            
        #     # products = products.filter( Q( Q(discounted_price = None) & Q(price__range=(min_price,max_price)) ) | Q(discounted_price__range=(min_price,max_price)) )


        if request.user.is_authenticated:
            user = request.user
            liked = Article_Like.objects.filter(user=user)
            likedd = []
            for like in liked:
                likedd.append(like.post)
            for post in products:
                if post in likedd:
                    post.liked = True
        # productss = []
        # for pr in products:
        #     productss.append(pr)
        # for i in range(12):
        #     if products:
        #         productss.append(products[0])

        max_price = products.aggregate(Max('price'))['price__max']
        max_discounted_price = products.aggregate(Max('discounted_price'))['discounted_price__max']

        # Get the overall maximum value
        try:
            max_value = max(max_price, max_discounted_price)
            context['prix_max'] = max_value

        except:
            context['no_prix_max'] = 'no_prix_max'
        context['products'] = products

    return render(request,"vintage/search.html",context)


def signup(request):
    context = {}
    context = categories(request, context)
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('/')
    else:
        form = UserCreationForm()
    context.update({'form':form})
    return render(request, 'vintage/signup.html', context)

def post(request, genre, category, product_name):
    context = {}
    context = categories(request, context)
    category = Category.objects.get(name=category)
    product = Post.objects.get(title=product_name, genre= genre, category= category)
    if request.user.is_authenticated:
        user = request.user
        liked = Article_Like.objects.filter(user=user)
        likedd = []
        for like in liked:
            likedd.append(like.post)
        if product in likedd:
            product.liked = True

    images = PostPicture.objects.filter(post=product)
    context.update({'product':product,'images':images})

    return render(request,"vintage/post.html",context)

def page(request, username):
    context = {}
    context = categories(request, context)
    his_user = User.objects.get(username=username)
    profile = Profile.objects.get(user=his_user)
    products = Post.objects.filter(seller=his_user, deleted=False)
    nb_posts = products.count()
    if request.user.is_authenticated:
        user = request.user
        liked = Article_Like.objects.filter(user=user)
        likedd = []
        for like in liked:
            likedd.append(like.post)
        for post in products:
            if post in likedd:
                post.liked = True

    context.update({'profile':profile,'products':products,'nb_posts':nb_posts})
    if request.user.is_authenticated:
        user = request.user
        if Abonnement.objects.filter(follower=user, followed=his_user).exists():
            context.update({'followed':'followed'})
        if user == his_user:
            context.update({'my_profile':'my_profile'})
        if Abonnement.objects.filter(follower=his_user, followed=user).exists():
            context.update({'followed_me':'followed_me'})
    return render(request,"vintage/page.html",context)

@login_required
def report(request, user_id):
    context = {}
    context = categories(request, context)
    user = request.user
    report_user = User.objects.get(username=user_id)

    context.update({'report_user':report_user})
    if request.method == "POST":
        if request.POST.get('comment'):
            if Signal.objects.filter(reporter=user, reported=report_user).count() >= 3:
                error_message = "Vous avez déja signalé cet utilisateur 3 fois"
                context.update({'error_message':error_message})
                return render(request,"vintage/signal.html",context)

            comment = request.POST.get('comment')
            if request.FILES.get('screenshot'):
                screenshot = request.FILES.get('screenshot')
                report = Signal.objects.create(reporter=user, reported=report_user, comment=comment, screenshot=screenshot)
            else:
                report = Signal.objects.create(reporter=user, reported=report_user, comment=comment)
            report.save()
        return redirect(request.META.get('HTTP_REFERER', '/'))
    return render(request,"vintage/signal.html",context)

@login_required
def sell(request, product_id, other_user):
    sold_user = User.objects.get(username = other_user)
    product = Post.objects.get(id=product_id)
    transaction = Transaction.objects.create(user=sold_user, post=product)
    transaction.save()
    return redirect(request.META.get('HTTP_REFERER', '/'))


@login_required(login_url='/login/')
def chat(request, other_user, product_id):
    context = {}
    context = categories(request, context)
    user = request.user
    if product_id != 'inbox' and other_user != 'inbox':
        other_user = User.objects.get(username=other_user)
    profile = Profile.objects.get(user=user)
    if request.method == "POST":
            
        if request.POST.get('message'):
            message = request.POST.get('message')
            post = Post.objects.get(id=product_id)
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
        last_message = chat.message
        if len(last_message) > 20:
            last_message = last_message[:20] + "..."
        conversation = {
            'post': chat.post,
            'other_user': other_userr,
            'last_message': last_message,
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
        context.update({'inbox':'inbox'})
    else:
        product = Post.objects.get(id=product_id)
        transaction = Transaction.objects.filter(post=product).first()
        print(transaction)
        if transaction:
            if request.method == "POST" and not transaction.note:
                if request.POST.get('rating'):
                    rating = int(request.POST.get('rating'))
                    if rating > 0 and rating <= 5:
                        transaction.note = rating
                        if request.POST.get('comment'):
                            comment = request.POST.get('comment')
                            transaction.comment = comment
                        transaction.save()
            context.update({'transaction':transaction})
        messages = Chat.objects.filter( Q(Q(sender=user) & Q(receiver=other_user)) | Q(Q(sender=other_user) & Q(receiver=user)) , post=product).order_by('timestamp')
        context.update({'product':product, 'other_user': other_user, 'messages':messages})


    context.update({'profile':profile})
    return render(request,"vintage/chat.html",context)

def category(request, genre, category):
    context = {}
    context = categories(request, context)
    if category != "all":
        category = Category.objects.get(name=category)
        products = Post.objects.filter(category=category, genre=genre, deleted=False)
    else:
        products = Post.objects.filter(genre=genre, deleted=False)
    context.update({'products':products,'category':category,'genre':genre})
    return render(request,"vintage/category.html",context)
def customnotfound(request, exception):
    context = {}
    context = categories(request, context)
    return render(request, "vintage/404.html",context)
def customserver(request):
    context = {}
    context = categories(request, context)
    return render(request, "vintage/500.html",context)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView
from django.urls import reverse_lazy

# Password Change
@method_decorator(login_required, name='dispatch')
class CustomPasswordChangeView(PasswordChangeView):
    template_name = 'vintage/password_change.html'
    success_url = '/profile/'

@method_decorator(login_required, name='dispatch')
class CustomPasswordChangeDoneView(PasswordChangeDoneView):
    def get_success_url(self):
        return reverse_lazy('profile')  # Replace 'home' with the name of your home page URL pattern