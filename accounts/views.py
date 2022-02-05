from django.shortcuts import render, redirect
from django.core.mail import send_mail

# Create your views here.
def send_login_email(request):
    email = request.POST['email']
    send_mail(
        'Your login link for Superlist', 
        'body', 
        'noreply@superlist', 
        [email]
    )
    return redirect('/')
