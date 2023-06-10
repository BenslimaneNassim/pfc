from .models import *

def categories(request, context):
    categories = Category.objects.all()
    context['categories'] = categories
    if request.user.is_authenticated:
        if Article_Panier.objects.filter(user=request.user).exists():
            carts = Article_Panier.objects.filter(user=request.user)
            cart_products = Post.objects.filter(id__in=carts.values_list('post', flat=True))
            context['cart_products'] = cart_products
    return context