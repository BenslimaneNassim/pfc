from .models import *

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
    return context

import colorsys

import colorsys

def get_color(decimal):
    # Map the decimal number to a value between 0 and 1
    normalized_decimal = decimal / 5.0

    # Convert the normalized decimal to Hue (H) value between 0 and 1
    hue = normalized_decimal

    # Set the saturation (S) and value (V) to fixed values
    saturation = 1.0
    value = 1.0

    # Convert HSV to RGB
    rgb = colorsys.hsv_to_rgb(hue, saturation, value)

    # Convert RGB to hexadecimal format
    hex_color = '#{:02x}{:02x}{:02x}'.format(
        int(rgb[0] * 255), int(rgb[1] * 255), int(rgb[2] * 255))

    return hex_color

