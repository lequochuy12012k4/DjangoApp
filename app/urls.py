from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomePage, name=''),
    path('login', views.LoginPage, name='login'),
    path('register', views.RegisterPage, name='register'),
    path('forgot-password', views.ForgotPasswordPage, name='forgot-password'),
    path('reset-password', views.ResetPasswordPage, name='reset-password'),
    path('profile', views.ProfilePage, name='profile'),
    path('upload', views.UploadPage, name='upload'),
    path('favorite', views.FavoritePage, name='favorite'),
]
