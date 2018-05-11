"""jimedol URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path,include,re_path
import xadmin
from django.views.generic import TemplateView
from users.views import loginView,registerView,ActiveUserView,ForgetPwdView,ResetView,ResetPwdView

from django.views.static import serve
from jimedol.settings import MEDIA_ROOT


urlpatterns = [
    path('xadmin/', xadmin.site.urls),
    path('', TemplateView.as_view(template_name="index.html"),name="index"),
    path('login/',loginView.as_view(),name="login"),
    path('register/',registerView.as_view(),name="register"),
    path('captcha/', include('captcha.urls')),
    re_path('active/(?P<active_code>.*)/',ActiveUserView.as_view(),name="user_active"),
    path('forgetpwd/',ForgetPwdView.as_view(),name="forgetpwd"),
    re_path('reset/(?P<active_code>.*)/',ResetView.as_view(),name="reset_pwd"),
    path('resetpwd/',ResetPwdView.as_view(),name="resetpwd"),
    # 课程机构url
    path('org/', include('organization.urls',namespace='org')),

    # 处理图片地址
    re_path('media/(?P<path>.*)',serve,{"document_root":MEDIA_ROOT}),
    # course的url
    path('courses/',include('courses.urls',namespace='courses'))


    # cookie:{"key":sss}

]
