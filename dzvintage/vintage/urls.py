from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('',views.index,name='index'),
    path('category/<str:genre>/<str:category>/',views.category,name='category'),
    path('category/<str:genre>/<str:category>/<str:product_name>/',views.post, name='post'),
    path('chat/<str:other_user>/<str:product_id>/',views.chat,name='chat'),
    path("search/",views.search,name="search"),
    path('login/', auth_views.LoginView.as_view(template_name='vintage/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('signup/', views.signup, name='signup'),

]