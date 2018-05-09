# form验证例如长度之类的

from django import forms
from captcha.fields import CaptchaField


class LoginForm(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(required=True,min_length=5)


class registerForm(forms.Form):
    email = forms.EmailField(required=True)
    password = forms.CharField(required=True,min_length=5)
    captcha = CaptchaField(error_messages={"invalid":"验证码错误"})

class ForgetForm(forms.Form):
    email = forms.EmailField(required=True)

    captcha = CaptchaField(error_messages={"invalid":"验证码错误"})


class ResetPwdForm(forms.Form):

    password = forms.CharField(required=True,min_length=5)
    cpassword = forms.CharField(required=True,min_length=5)
