from .models import *
from django.conf import settings
from django.core.mail import send_mail

def categories(request, context):
    categories = Category.objects.all()
    for category in categories:
        category.nb_products = Post.objects.filter(category=category, deleted=False).count()
    context['categories'] = categories
    if request.user.is_authenticated:
        if Article_Panier.objects.filter(user=request.user).exists():
            carts = Article_Panier.objects.filter(user=request.user)
            cart_products = Post.objects.filter(id__in=carts.values_list('post', flat=True))
            context['cart_products'] = cart_products
    #check newsletter form:
    if request.method == 'POST' and request.POST.get('email'):

        email = request.POST.get('email')
        if not Newsletter.objects.filter(email=email).exists():
            newsletter = Newsletter()
            newsletter.email = email
            newsletter.save()
            send_newsletter_subscribing_email(email)
            

    return context


def send_greeting_email(email, username):
    subject = 'Bienvenue sur DZVintage'
    message = f'Bonjour {username},\n\nMerci de vous être inscrit à DZVintage. Nous espérons que vous apprécierez notre site Web.\n\nCordialement,\nL\'équipe DZVintage'
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, from_email, recipient_list, fail_silently=False)

def send_newsletter_subscribing_email(email):
    subject = 'Bienvenue à notre newsletter'
    message = f'Bonjour {email},\n\nMerci de vous être inscrit à notre newsletter. Nous espérons que vous apprécierez notre site Web.\n\nCordialement,\nL\'équipe DZVintage'
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, from_email, recipient_list, fail_silently=False)

def confirm_phone_number(first_name, phone_number):
    profile = Profile.objects.filter(phone_number=phone_number).first()
    if profile:
        if not profile.phone_confirmed:
            profile.phone_confirmed = True
            message_reply = (f'Merci, {first_name}! Votre numéro {phone_number} a été confirmé.\nVous êtes maintenant un utilisateur vérifié')
            return message_reply
        elif profile.phone_confirmed:
            message_reply = (f'{first_name} Votre numéro {phone_number} a déja été confirmé.\nVous êtes un utilisateur vérifié')
            return message_reply
    else:
        message_reply = (f'{first_name} Votre profile n\'existe pas! \nCréez un compte sur vintagedz.pythonanywhere.com/login')
        return message_reply
