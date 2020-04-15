from django import forms

# 图形验证码
from captcha.fields import CaptchaField

class LoginForm(forms.Form):
    """
    登录验证表单
    """
    # 用户名密码不能为空
    username = forms.CharField(required=True)
    password = forms.CharField(required=True, min_length=3)

class RegisterForm(forms.Form):
    """
    注册验证表单
    """
    email = forms.EmailField(required=True)
    password = forms.CharField(required=True, min_length=3)
    captcha = CaptchaField()

class ForgetPwdForm(forms.Form):
    """
    忘记密码表单
    """
    email = forms.EmailField(required=True)
    captcha = CaptchaField(error_messages={'invalid': 'Invalid captcha.'})


class ModifyPwdForm(forms.Form):
    """
    重置密码
    """
    password1 = forms.CharField(required=True, min_length=3)
    password2 = forms.CharField(required=True, min_length=3)