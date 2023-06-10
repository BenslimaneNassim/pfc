from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('',views.index,name='index'),
    path("produits/<str:cat>/",views.products,name="products"),
    path("profile/",views.profile,name="profile"),
    path("report/<str:user_id>/",views.report,name="report"),
    path("profile/annonces/",views.annonces,name="annonces"),
    path("profile/annonces/vendre/<str:product_id>/<str:other_user>/",views.sell,name="sell"),
    path("profile/annonces/ajouter/",views.add,name="add"),
    path("profile/annonces/supprimer/<str:product_id>/",views.delete,name="delete"),
    path("profile/annonces/supprimer_pic/<str:pic_id>/",views.delete_pic,name="delete_pic"),
    path("profile/page/<str:username>/",views.page,name="page"),
    path("profile/annonces/modifier/<str:product_id>/",views.modify,name="modify"),
    path('category/<str:genre>/<str:category>/',views.category,name='category'),
    path('category/<str:genre>/<str:category>/<str:product_name>/',views.post, name='post'),
    path('chat/<str:other_user>/<str:product_id>/',views.chat,name='chat'),
    path('follow/<str:username>/',views.follow,name='follow'),
    path('change_panier/<str:product_id>/',views.change_panier,name='change_panier'),
    path('likeit/<str:product_id>/',views.likeit,name='likeit'),
    path("search/",views.search,name="search"),
    path('login/', auth_views.LoginView.as_view(template_name='vintage/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('signup/', views.signup, name='signup'),
    path('profile/password_change/', views.CustomPasswordChangeView.as_view(), name='password_change'),
    path('profile/password_change/done/', views.CustomPasswordChangeDoneView.as_view(), name='password_change_done'),

]