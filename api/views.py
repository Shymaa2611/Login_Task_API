from django.shortcuts import render,redirect
import random
from django.contrib.auth.models import User
from rest_framework.decorators import api_view,permission_classes,authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from django.conf import settings
from django.core.mail import send_mail


@api_view(['POST'])
def Login(request):
    email = request.data['email']
    password=request.data['password']
    try:
        user = User.objects.get(email=email)
        return Response({
            'redirect_url': '/home/',
            'username': user.username
        })
    except User.DoesNotExist:
        return Response({'redirect_url': '/signup/'})

@api_view(['POST'])
def signup(request):
    username = request.data['username']
    email = request.data['email']
    password = request.data['password']
    user = User.objects.create_user(username=username, email=email, password=password)
    user.save()
    code = ''.join([str(random.randint(0, 9)) for _ in range(4)])
    request.session['verification_code'] = code
    request.session['email'] = email
    subject = 'Verification code for your account'
    message = f'Your verification code is: {code}'
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, from_email, recipient_list,fail_silently=False)

    return Response({'redirect_url': '/verified/', 'username': user.username})



@api_view(['POST'])
def verify(request):
    code = request.data['code']
    expected_code = request.session.get('verification_code', '')
    email = request.session.get('email', '')
    user = User.objects.get(email=email, is_active=True)
    print("expected code = ", expected_code)
    if code == expected_code:
        return Response({
            'redirect_url': '/home/',
            'message': 'Successfully',
            'username': user.username
        })
    else:
        return Response({'error': 'Verification code is incorrect'})