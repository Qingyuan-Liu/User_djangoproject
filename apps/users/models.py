from datetime import datetime
from django.db import models
from django.contrib.auth.models import AbstractUser


class UserProfile(AbstractUser):
    """
    用户信息
    通过 AbstractUser 继承 django 原有自带的 User 类
    """
    gender_choices = (
        ('male', '男'),
        ('female', '女'),
    )
    nick_name = models.CharField('Nickname', max_length=50, default='')
    birthday = models.DateField('Birthday',null=True,blank=True)
    gender = models.CharField('Gender',max_length=10,choices=gender_choices,default='female')
    adress = models.CharField('Address',max_length=100,default='')
    mobile = models.CharField('Mobile',max_length=11,null=True,blank=True)
    login_sta = models.CharField(u'lock', max_length=2, default=0)
    login_suo = models.DateTimeField('locking time',null=True, blank=True)
    pass_errnum=models.IntegerField(u'times of the user entering password',default=0)

    class Meta:
        verbose_name = 'UserProfile'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username


class EmailVerifyRecord(models.Model):
    """
    图形验证码
    """
    send_choices = (
        ('register','注册'),
        ('forget','找回密码')
    )

    code = models.CharField('验证码',max_length=20)
    email = models.EmailField('邮箱',max_length=50)
    send_type = models.CharField(choices=send_choices,max_length=10)
    send_time = models.DateTimeField(default=datetime.now)

    class Meta:
        verbose_name = 'Captcha'
        verbose_name_plural = verbose_name
