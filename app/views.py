from django.http import HttpResponse
from django.template import loader
from .models import *

def HomePage(request):
  template = loader.get_template('HomePage.html')
  return HttpResponse(template.render())

def LoginPage(request):
  template = loader.get_template('authentication/Login.html')
  return HttpResponse(template.render())

def RegisterPage(request):
  template = loader.get_template('authentication/Register.html')
  return HttpResponse(template.render())

def ForgotPasswordPage(request):
  template = loader.get_template('authentication/ForgotPassword.html')
  return HttpResponse(template.render())

def ResetPasswordPage(request):
  template = loader.get_template('authentication/ResetPassword.html')
  return HttpResponse(template.render())

def ProfilePage(request):
  template = loader.get_template('Navbar/ProfilePage.html')
  return HttpResponse(template.render())

def UploadPage(request):
  template = loader.get_template('Navbar/UploadPage.html')
  return HttpResponse(template.render())

def FavoritePage(request):
  template = loader.get_template('Navbar/FavoritePage.html')
  return HttpResponse(template.render())