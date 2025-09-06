from django.urls import path
from .views import *

urlpatterns = [
    path('', HomePage, name='home'),
    path('document/<int:document_id>/', DocumentDetailPage, name='document-detail'),
    path('login/', LoginPage, name='login'),
    path('register/', RegisterPage, name='register'),
    path('logout/', LogoutUser, name='logout'),
    path('forgot-password/', ForgotPasswordPage, name='forgot-password'),
    path('reset-password/', ResetPasswordPage, name='reset-password'),
    path('profile/', ProfilePage, name='profile'),
    path('upload/', UploadPage, name='upload'),
    path('favorite/<int:document_id>/', ToggleFavorite, name='toggle-favorite'),
    path('favorites/', FavoritePage, name='favorites'),
    path('search/', Search, name='search'),
]
