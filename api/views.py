from django.shortcuts import render
import random
from django.contrib.auth.models import User
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.conf import settings
from django.core.mail import send_mail

@api_view(['POST'])
def Login(request):
    email = request.data['email']
    user=request.user
    if User.objects.filter(email=email).exists():
        return Response({'redirect_url': '/home/','username':user.username
                         
             })
    else:
        return Response({'redirect_url': '/signup/'})
@api_view(['POST'])
def signup(request):
    username = request.data['username']
    email = request.data['email']
    password = request.data['password']
    user = User.objects.create_user(username=username, email=email, password=password)
    user.save()
    code = ''.join([str(random.randint(0, 9)) for _ in range(4)])
    subject = 'Verification code for your account'
    message = f'Your verification code is: {code}'
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, from_email, recipient_list,fail_silently=False)

    return Response({'redirect_url': '/Verified/', 'username': user.username})