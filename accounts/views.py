from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib import messages

# Create your views here.
def send_login_email(request):
    email = request.POST['email']
    send_mail(
        'Your login link for Superlists', 
        'body', 
        'noreply@superlist', 
        [email]
    )
    messages.success(
       request,
       "Check your email, we've sent you a link you can use to log in."
    )
    return redirect('/')


def login(request):
    return redirect('/')
