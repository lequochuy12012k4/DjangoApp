from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomePage, name=''),
    path('/register', views.RegisterPage, name='register'),
    path('/login', views.LoginPage, name='login'),
    path('/profile', views.ProfilePage, name='profile'),
    path('/upload', views.UploadPage, name='upload'),
    path('/favorite', views.FavoritePage, name='favorite'),
]
