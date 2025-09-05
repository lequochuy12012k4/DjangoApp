from django.http import HttpResponse
from django.template import loader

def HomePage(request):
  template = loader.get_template('HomePage.html')
  return HttpResponse(template.render())

def LoginPage(request):
  template = loader.get_template('authentication/Login.html')
  return HttpResponse(template.render())

def RegisterPage(request):
  template = loader.get_template('authentication/Register.html')
  return HttpResponse(template.render())

def ProfilePage(request):
  template = loader.get_template('Navbar/Profile.html')
  return HttpResponse(template.render())