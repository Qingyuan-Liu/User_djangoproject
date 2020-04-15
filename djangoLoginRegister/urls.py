"""djangoLoginRegister URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from django.contrib import admin
from django.urls import include

from django.conf.urls import url
from django.contrib import admin
from django.urls import path
from users.views import LoginView, LogoutView, RegisterView, ActiveUserView, ForgetPwdView,ResetView,ModifyPwdView,IndexView

from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    url('^$', TemplateView.as_view(template_name='index.html'), name='index'),
    url('^login/$', LoginView.as_view(), name='login'),
    url('^logout/$', LogoutView.as_view(), name='logout'),
    url('^index/$', IndexView.as_view(), name='home'),
    url('^register/$', RegisterView.as_view(), name='register'),
    url('captcha/', include('captcha.urls')),
    url(r'^active/(?P<active_code>.*)/$', ActiveUserView.as_view(), name="user_active"),
    # 忘记密码
    url('^forget/$', ForgetPwdView.as_view(), name='forget_pwd'),
    # 重置密码时发送的邮箱链接
    url(r'^reset/(?P<active_code>.*)/$', ResetView.as_view(), name="reset_pwd"),
    # 重置密码
    url('^modify_pwd/$', ModifyPwdView.as_view(), name='modify_pwd'),
]
