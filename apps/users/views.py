from django.http import HttpResponse
from django.views import View
from users.models import UserProfile, EmailVerifyRecord
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import logout
from django.contrib.auth import views as auth_views
from django.shortcuts import render
from users.forms import LoginForm, RegisterForm,ForgetPwdForm,ModifyPwdForm
from utils.email_send import send_register_email
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import make_password
from django.contrib.auth import logout as auth_logout
from users.models import UserProfile
from django.contrib.auth.mixins import LoginRequiredMixin
import datetime
import pytz

class LogoutView(auth_views.LogoutView):
    def get(self, request, *args, **kwargs):
        auth_logout(request)
        return HttpResponseRedirect('/login/')

class IndexView(LoginRequiredMixin,View):
    def get(self,request):
        return render(request,'index.html')

class LoginView(View):
    def get(self,request):
        return render(request, 'login.html')

    def post(self,request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user_name = request.POST.get('username', '')
            pass_word = request.POST.get('password', '')
            print('user_name：', user_name)
            print('pass_word：', pass_word)
            # try:
            user_list = UserProfile.objects.filter(username = user_name)
            if not user_list:
                return render(request, 'login.html', {'msg': 'Username is not exists', 'login_form':login_form})
            user=user_list[0]
            if not user.is_active:
                print('Email address not activated, login failed')
                return render(request, 'login.html', {'msg': 'The email address is not activated, failed to login', 'login_form':login_form})
            now=datetime.datetime.now()
            if user.login_sta==True and ((now.replace(tzinfo=pytz.timezone('UTC'))-user.login_suo).total_seconds() <600):
                return render(request, 'login.html', {'msg': 'The account is locked'})
            # now=datetime.datetime.now()
            # if (now.replace(tzinfo=pytz.timezone('UTC'))-user.login_suo).total_seconds() <600:
            #     return render(request, 'login.html', {'msg': 'The account is locked for 10 mins!'})
            if user.pass_errnum>10:
                user.pass_errnum=0
                user.login_suo=datetime.datetime.now()
                user.login_sta=True
                user.save()
                return render(request, 'login.html', {'msg': 'Enter the wrong password for 10 times, please try to login 10 minutes later'})

            user_auth = authenticate(username=user_name, password=pass_word)
            if user_auth is not None:
                user.last_login=datetime.datetime.now()
                user.login_sta=False
                user.pass_errnum=0
                user.save()
                login(request, user)
                return HttpResponseRedirect('/index/')
                # return render(request, 'index.html', {'name': user_name})
            user.pass_errnum+=1
            user.save()
            return render(request, 'login.html', {'msg': 'Wrong password'})
            # except:
            #     return render(request, 'login.html', {'msg': 'Username is not exists', 'login_form':login_form})
        else:
            return render(request, 'login.html', {'login_form':login_form})


class RegisterView(View):
    def get(self,request):
        register_form = RegisterForm()
        return render(request, 'register.html', {'register_form': register_form})

    def post(self, request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            user_name = request.POST.get('email', '')
            # 用户已存在
            if UserProfile.objects.filter(email = user_name):
                return render(request, 'register.html', {'register_form': register_form, 'msg': 'The username is already existed.'})

            pass_word = request.POST.get('password', '')

            print('user_name：', user_name)
            print('pass_word：', pass_word)

            # 实例化一个 useProfile 对象
            user_profile = UserProfile()
            user_profile.username = user_name
            user_profile.email = user_name
            # 默认添加的用户是激活状态（is_active=1表示True），这里修改默认的状态为 False，只有用户邮箱激活后才改为True
            user_profile.is_active = False
            # 密码加密
            user_profile.password = make_password(pass_word)
            user_profile.save()
            send_register_email(user_name, 'register')
            return render(request, 'login.html')
        else:
            return render(request, 'register.html', {'register_form': register_form})

class ActiveUserView(View):
    """
    激活邮件
    """
    def get(self, request, active_code):
        # 查询邮箱验证记录是否存在
        all_record = EmailVerifyRecord.objects.filter(code=active_code)

        if all_record:
            for record in all_record:
                # 获取到对应邮箱
                email = record.email
                # 查找到邮箱对应的 user
                user = UserProfile.objects.get(email=email)
                user.is_active = True
                user.save()
        # 验证码不对的时候跳转到激活失败页面
        else:
            return render(request, 'register.html')

        # 激活成功 跳转到登录页面
        return render(request, 'login.html')

class ForgetPwdView(View):
    """
    找回密码
    """
    def get(self,request):
        forget_form = ForgetPwdForm()
        return render(request,'forgetpwd.html',{'forget_form':forget_form})

    def post(self, request):
        forget_form = ForgetPwdForm(request.POST)
        if forget_form.is_valid():
            email = request.POST.get('email', '')
            send_register_email(email, 'forget')
            return render(request, 'login.html')
        else:
            return render(request, 'forgetpwd.html', {'forget_form': forget_form})


class ResetView(View):
    """
    打开邮箱链接
    """
    def get(self, request, active_code):
        # 查询邮箱验证记录是否存在
        all_record = EmailVerifyRecord.objects.filter(code=active_code)

        if all_record:
            for record in all_record:
                email = record.email
                return render(request, 'password_reset.html', {'email': email})

        # 验证码不对的时候跳转到激活失败页面
        else:
            return render(request, 'active_fail.html')
        return render(request, 'login.html')



class ModifyPwdView(View):
    """
    重置密码
    """
    def post(self, request):
        modify_form = ModifyPwdForm(request.POST)
        if modify_form.is_valid():
            pwd1 = request.POST.get('password1', '')
            pwd2 = request.POST.get('password2', '')
            email = request.POST.get('email', '')

            if pwd1 != pwd2:
                return render(request, 'password_reset.html', {'email': email, 'msg': 'The two passwords are not the same'})

            user = UserProfile.objects.get(email = email)
            user.password = make_password(pwd2)
            user.save()

            return render(request, 'login.html')

        else:
            email = request.POST.get('email', '')
            return render(request, 'password_reset.html', {'email': email, "modify_form": modify_form})