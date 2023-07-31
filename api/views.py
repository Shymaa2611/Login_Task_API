from django.shortcuts import render,redirect
import random
from django.contrib.auth.models import User
from rest_framework.decorators import api_view,permission_classes,authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm,verifiedForm,LoginForm
from .models import VerifyCodeM


# @api_view(['POST'])
# def Login(request):
#     email = request.data['email']
#     password=request.data['password']
#     try:
#         user = User.objects.get(email=email)
#         return Response({
#             'redirect_url': '/home/',
#             'username': user.username
#         })
#     except User.DoesNotExist:
#         return Response({'redirect_url': '/signup/'})

# @api_view(['POST'])
# def signup(request):
#     username = request.data['username']
#     email = request.data['email']
#     password = request.data['password']
#     user = User.objects.create_user(username=username, email=email, password=password)
#     user.save()
#     code = ''.join([str(random.randint(0, 9)) for _ in range(4)])
#     request.session['verification_code'] = code
#     request.session['email'] = email
#     subject = 'Verification code for your account'
#     message = f'Your verification code is: {code}'
#     from_email = settings.EMAIL_HOST_USER
#     recipient_list = [email]
#     send_mail(subject, message, from_email, recipient_list,fail_silently=False)

#     return Response({'redirect_url': '/verified/', 'username': user.username})



# @api_view(['POST'])
# def verify(request):
    # code = request.data['code']
    # expected_code = request.session.get('verification_code', '')
    # email = request.session.get('email', '')
    # user = User.objects.get(email=email, is_active=True)
    # print("expected code = ", expected_code)
    # if code == expected_code:
    #     return Response({
    #         'redirect_url': '/home/',
    #         'message': 'Successfully',
    #         'username': user.username
    #     })
    # else:
    #     return Response({'error': 'Verification code is incorrect'})
def home(request):
    username = request.session.get('username', None)
    context = {'username': username}
    return render(request,'home.html',context)

def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            if User.objects.filter(email=email).exists():
                return redirect('home')
            else:
                return redirect('signUp')
    else:
        form = LoginForm()
    context = {'form': form}
    return render(request, 'log_in.html', context)


def signUp(request):
    if request.method=='POST':
        form=SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data['email']
            #password = request.data['password']
            code = ''.join([str(random.randint(0, 9)) for _ in range(4)])
            request.session['verification_code'] = code
            request.session['username'] = form.cleaned_data['username']
            subject = 'Verification code for your account'
            message = f'Your verification code is: {code}'
            from_email = settings.EMAIL_HOST_USER
            recipient_list = [email]
            send_mail(subject, message, from_email, recipient_list,fail_silently=False)
            return redirect('verify')
    else:
            form=SignUpForm()
    context={
        'form':form
    }
    return render(request,'sign_up.html',context)




def verify(request):
    verification_code = request.session.get('verification_code')
    if request.method == 'POST':
        form = verifiedForm(request.POST)
        if form.is_valid():
            submitted_code = form.cleaned_data['code']
            if submitted_code == verification_code:
                username = request.session.get('username')

                user, created = User.objects.get_or_create(username=username, defaults={
                    'password': 'default_password',
                    'first_name': '',
                    'last_name': ''
                })

                verify_code = VerifyCodeM.objects.create(user=user, code=verification_code)

                request.session['username'] = username

                return redirect('home')
            else:
                return redirect('signUp')
    else:
        form = verifiedForm()
    context = {'form': form}
    return render(request, 'chick_email.html', context)