from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import *
from django.http import JsonResponse
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.urls import reverse
from django.utils.html import format_html

def HomePage(request):
  documents = Document.objects.all()
  context = {
    'documents': documents
  }
  return render(request, 'HomePage.html', context)

def DocumentDetailPage(request, document_id):
    document = get_object_or_404(Document, id=document_id)
    context = {
        'document': document
    }
    return render(request, 'DocumentDetailPage.html', context)

def LoginPage(request):
  if request.method == 'POST':
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = authenticate(request, username=username, password=password)
    if user is not None:
      login(request, user)
      messages.success(request, f'Welcome back, {user.username}!')
      return redirect('/')
    else:
      messages.error(request, 'Invalid username or password')
      return redirect('login')
  return render(request, 'authentication/Login.html')

def RegisterPage(request):
  if request.method == 'POST':
    username = request.POST.get('username')
    email = request.POST.get('email')
    password = request.POST.get('password')
    if User.objects.filter(username=username).exists():
      messages.error(request, 'Username already exists')
      return redirect('register')
    user = User.objects.create_user(username=username, email=email, password=password)
    user.save()
    messages.success(request, 'Account created successfully! You can now log in.')
    return redirect('login')
  return render(request, 'authentication/Register.html')

def LogoutUser(request):
  logout(request)
  return redirect('login')

def ForgotPasswordPage(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request, 'User with this email does not exist.')
            return redirect('forgot-password')

        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        reset_link = request.build_absolute_uri(reverse('reset-password', kwargs={'uidb64': uid, 'token': token}))

        messages.success(request, format_html('Password reset link: <a href="{}">{}</a>', reset_link, reset_link))
        return redirect('forgot-password')

    return render(request, 'authentication/ForgotPassword.html')

def ResetPasswordPage(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            new_password = request.POST.get('new_password')
            confirm_password = request.POST.get('confirm_password')
            if new_password != confirm_password:
                messages.error(request, "Passwords do not match.")
                return redirect(request.path)
            user.set_password(new_password)
            user.save()
            messages.success(request, "Password has been reset successfully. You can now log in.")
            return redirect('login')
        return render(request, 'authentication/ResetPassword.html')
    else:
        messages.error(request, "Invalid reset link.")
        return redirect('forgot-password')

@login_required(login_url='login')
def ProfilePage(request):
    if request.method == 'POST':
        user = request.user
        new_username = request.POST.get('username')
        new_password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if new_username and new_username != user.username:
            if User.objects.filter(username=new_username).exists():
                messages.error(request, 'Username already exists.')
                return redirect('profile')
            user.username = new_username

        if new_password:
            if new_password != confirm_password:
                messages.error(request, 'Passwords do not match.')
                return redirect('profile')
            user.set_password(new_password)

        user.save()
        login(request, user)  # Re-login the user
        messages.success(request, 'Profile updated successfully!')
        return redirect('profile')
    return render(request, 'Navbar/ProfilePage.html')

@login_required(login_url='login')
def UploadPage(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        author = request.POST.get('author')
        description = request.POST.get('description')
        image = request.FILES.get('image')
        file = request.FILES.get('file')
        if title and author and description and image and file:
            Document.objects.create(
                title=title,
                author=author,
                description=description,
                image=image,
                document=file
            )
            messages.success(request, 'Document uploaded successfully!')
            return redirect('upload')
        else:
            messages.error(request, 'Please provide all fields.')
    return render(request, 'Navbar/UploadPage.html')

@login_required(login_url='login')
def ToggleFavorite(request, document_id):
    document = get_object_or_404(Document, id=document_id)
    if request.user in document.favorited_by.all():
        document.favorited_by.remove(request.user)
        messages.success(request, 'Removed from favorites.')
    else:
        document.favorited_by.add(request.user)
        messages.success(request, 'Added to favorites.')
    return redirect(request.META.get('HTTP_REFERER', '/'))

@login_required(login_url='login')
def FavoritePage(request):
    favorite_documents = request.user.favorite_documents.all()
    context = {
        'documents': favorite_documents
    }
    return render(request, 'Navbar/FavoritePage.html', context)

def Search(request):
    query = request.GET.get('q')
    if query:
        documents = Document.objects.filter(title__icontains=query)
    else:
        documents = Document.objects.all()
    
    data = []
    for document in documents:
        data.append({
            'id': document.id,
            'title': document.title,
            'author': document.author,
            'description': document.description,
            'image_url': document.image.url,
            'document_url': document.document.url,
            'is_favorite': request.user in document.favorited_by.all() if request.user.is_authenticated else False
        })
    
    return JsonResponse(data, safe=False)
