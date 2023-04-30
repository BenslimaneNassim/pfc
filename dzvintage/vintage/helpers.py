from .models import *

def categories(context):
    categories = Category.objects.all()
    context['categories'] = categories
    return context