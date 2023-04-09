from django.contrib import admin
from .models import *

admin.site.register(Profile)
admin.site.register(Category)
admin.site.register(Post)
admin.site.register(PostPicture)
admin.site.register(Transaction)
admin.site.register(Chat)