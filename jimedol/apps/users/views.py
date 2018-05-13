from django.shortcuts import render
import json
from django.contrib.auth import authenticate,login
from django.http import HttpResponse
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.contrib.auth.hashers import make_password

# view类
from django.views.generic.base import View

from .models import UserProfile,EmailVerifyRecord
from .forms import LoginForm,registerForm,ForgetForm,ResetPwdForm,UploadImageForm
from utils.email_send import send_register_email
from utils.mixin_utils import LoginRequiredMixin

# Create your views here.
# 自定义登陆延展
class CustomBackend(ModelBackend):
    def authenticate(self,username=None,password=None,**kwargs):
        try:
            user = UserProfile.objects.get(Q(username=username)|Q(email=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


class loginView(View):
    def get(self,request):
        return render(request,'login.html',{})
    def post(self,request):
         login_form = LoginForm(request.POST)
         if login_form.is_valid():
              user_name = request.POST.get("username","")
              pass_word = request.POST.get("password","")
              user = authenticate(username=user_name,password=pass_word)
              if user is not None:
                  if user.is_active:
                     login(request,user)
                     return render(request,"index.html")
                  else:
                     return render(request,'login.html',{'msg':'用户未激活'})



              else:
                  return render(request,'login.html',{'msg':'用户名或密码错误'})



         else:
             return render(request,'login.html',{'login_form':login_form})


# 登陆接口
# def userLogin(request):
#      if request.method == "POST":
#          user_name = request.POST.get("username","")
#          pass_word = request.POST.get("password","")
#          user = authenticate(username=user_name,password=pass_word)
#          if user is not None:
#              login(request,user)
#              return render(request,"index.html")
#
#          else:
#              return render(request,'login.html',{'msg':'用户名或密码错误'})
#
#
#      elif request.method == "GET":
#          return render(request,"login.html",{})
# 注册
class registerView(View):
    def get(self, request):
        register_form = registerForm()
        return render(request, "register.html", {'register_form':register_form})

    def post(self, request):
        register_form = registerForm(request.POST)
        if register_form.is_valid():
            user_name = request.POST.get("email", "")
            if UserProfile.objects.filter(email=user_name):
                return render(request, "register.html", {'msg':'用户已经存在','register_form':register_form})


            pass_word = request.POST.get("password", "")
            user_profile = UserProfile()
            user_profile.username = user_name
            user_profile.email = user_name
            user_profile.is_active = False

            user_profile.password = make_password(pass_word)
            user_profile.save()



            send_register_email(user_name, "register")
            return render(request,"login.html",{})
        else:
            return render(request,"register.html",{'register_form':register_form})


class ActiveUserView(View):
    def get(self,request,active_code):
        all_records = EmailVerifyRecord.objects.filter(code=active_code)
        if all_records:
            for record in all_records:
                email = record.email
                user = UserProfile.objects.get(email=email)
                user.is_active = True
                user.save()


        return render(request,"login.html",{})

class ForgetPwdView(View):
    def get(self,request):
        forget_form = ForgetForm()
        return render(request,'forgetpwd.html',{'forget_form':forget_form})
    def post(self, request):
        forget_form = ForgetForm(request.POST)
        if forget_form.is_valid():
            email = request.POST.get("email", "")
            send_register_email(email, "forget")
            return render(request,'sendsuccess.html',{})
        else:
            return render(request,'forgetpwd.html',{'forget_form':forget_form})

class ResetView(View):
    def get(self,request,active_code):
        all_records = EmailVerifyRecord.objects.filter(code=active_code)
        if all_records:
            for record in all_records:
                email = record.email
                return render(request,"password_reset.html",{"email":email})




        return render(request,"login.html",{})

class ResetPwdView(View):

    def post(self,request):
        reset_form = ResetPwdForm(request.POST)
        if reset_form.is_valid():
            pwd = request.POST.get("password","")
            cpwd = request.POST.get("cpassword","")
            email = request.POST.get("email","")
            if pwd != cpwd:
                return render(request,"password_reset.html",{"email":email,"msg":"密码不一致"})
            user = UserProfile.objects.get(email = email)
            user.password = make_password(pwd)
            user.save()
            return render(request,"login.html",{})
        else:
            email = request.POST.get("email","")
            return render(request,"password_reset.html",{"email":email,"reset_form":reset_form})


class UserInfoView(LoginRequiredMixin,View):
    def get(self,request):
        # 用户个人信息
        return render(request,"usercenter-info.html",{})



class ImageUploadView(LoginRequiredMixin,View):
    def post(self,request):
        # 文件类型是放在request.files里面
        # 利用modelform的特点直接保存图片
        image_form = UploadImageForm(request.POST,request.FILES,instance=request.user)
        if image_form.is_valid():
            # image = image_form.cleaned_data['image']
            # request.user.image = image
            # request.user.save()
            image_form.save()
            return HttpResponse('{"status":"success", "msg":"保存成功"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail", "msg":"保存不成功"}', content_type='application/json')


class ChangePwdView(LoginRequiredMixin,View):
    # 在个人中心修改密码

    def post(self,request):
        reset_form = ResetPwdForm(request.POST)
        if reset_form.is_valid():
            pwd = request.POST.get("password","")
            cpwd = request.POST.get("cpassword","")

            if pwd != cpwd:
                return HttpResponse('{"status":"fail", "msg":"密码不一致"}', content_type='application/json')
            user = request.user
            user.password = make_password(pwd)
            user.save()
            return HttpResponse('{"status":"success", "msg":"修改成功"}', content_type='application/json')
        else:

            return HttpResponse(json.dumps(reset_form.errors), content_type='application/json')
