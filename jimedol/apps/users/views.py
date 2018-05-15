from django.shortcuts import render
import json
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.contrib.auth.hashers import make_password

# view类
from django.views.generic.base import View

from .models import UserProfile,EmailVerifyRecord,Banner
from operation.models import UserCourse,UserFavorite,UserMessage
from courses.models import Course
from organization.models import CourseOrg,Teacher
from .forms import LoginForm,registerForm,ForgetForm,ResetPwdForm,UploadImageForm,UserInfoForm
from utils.email_send import send_register_email
from utils.mixin_utils import LoginRequiredMixin
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger

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
                     from django.urls import reverse
                     return HttpResponseRedirect(reverse("index"))
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
            # 写入注册消息
            user_message = UserMessage()
            user_message.user = user_profile.id
            user_message.message= "欢迎注册"
            user_message.save()




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
    def post(self,request):
        # 必须指明instance
        user_form = UserInfoForm(request.POST,instance=request.user)
        if user_form.is_valid():
            user_form.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse(json.dumps(user_form.errors), content_type='application/json')






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



class SendEmailView(LoginRequiredMixin,View):
    # 发送邮箱验证码
    def get(self,request):
        email = request.GET.get('email','')
        if UserProfile.objects.filter(email=email):
            return HttpResponse('{"email":"邮箱已经注册"}', content_type='application/json')
        send_register_email(email, "update")
        return HttpResponse('{"status":"success", "msg":"发送成功"}', content_type='application/json')


class UpdateEmailView(LoginRequiredMixin,View):
    def post(self,request):
        email = request.POST.get('email','')
        code = request.POST.get('code','')
        existed_email = EmailVerifyRecord.objects.filter(email=email,code=code,send_type='update')
        if existed_email:
            user = request.user
            user.email= email
            user.save()
            return HttpResponse('{"status":"success", "msg":"修改成功"}', content_type='application/json')
        else:
            return HttpResponse('{"email":"验证码出错"}', content_type='application/json')



class MyCourseView(LoginRequiredMixin,View):
    # 个人课程
    def get(self,request):
        user_course = UserCourse.objects.filter(user=request.user)


        return render(request,'usercenter-mycourse.html',{
            'user_course':user_course

        })


class MyFavOrgView(LoginRequiredMixin,View):
    # 个人收藏机构
    def get(self,request):
        org_list = []
        user_fav_org = UserFavorite.objects.filter(user=request.user,fav_type=2)
        for fav_org in user_fav_org:
            org_id = fav_org.fav_id
            org = CourseOrg.objects.get(id=org_id)
            org_list.append(org)

        return render(request,'usercenter-fav-org.html',{
            'org_list':org_list

        })


class MyFavTeacherView(LoginRequiredMixin,View):
    # 个人收藏机构
    def get(self,request):
        teacher_list = []
        user_fav_teacher = UserFavorite.objects.filter(user=request.user,fav_type=3)
        for fav_teacher in user_fav_teacher:
            teacher_id = fav_teacher.fav_id
            teacher = Teacher.objects.get(id=teacher_id)
            teacher_list.append(teacher)

        return render(request,'usercenter-fav-teacher.html',{
            'teacher_list':teacher_list

        })

class MyFavCourseView(LoginRequiredMixin,View):
    # 个人收藏机构
    def get(self,request):
        course_list = []
        user_fav_course = UserFavorite.objects.filter(user=request.user,fav_type=1)
        for fav_course in user_fav_course:
            course_id = fav_course.fav_id
            course = Course.objects.get(id=course_id)
            course_list.append(course)

        return render(request,'usercenter-fav-course.html',{
            'course_list':course_list

        })


class MyMessageView(LoginRequiredMixin,View):
    def get(self,request):
        all_messages = UserMessage.objects.filter(user=request.user.id)
        all_unreadmessage = UserMessage.objects.filter(user=request.user.id,has_read = False)

        for unread_message in all_unreadmessage:
            unread_message.has_read = True
            unread_message.save()

        # 做分页
        try:
           page = request.GET.get('page', 1)
        except PageNotAnInteger:
           page = 1



    # Provide Paginator with the request object for complete querystring generation

        p = Paginator(all_messages, 5, request=request)

        messages = p.page(page)
        return render(request,'usercenter-message.html',{
          'all_messages':messages
        })


class LogoutView(View):
    def get(self,request):
        logout(request)
        from django.urls import reverse
        return HttpResponseRedirect(reverse("index"))



class IndexView(View):
    # 首页
    def get(self,request):
        # 取出轮播图
        all_banners = Banner.objects.all().order_by('index')
        course = Course.objects.filter(is_banner=False)[:6]
        banner_courses = Course.objects.filter(is_banner=False)[:3]
        courseorg = CourseOrg.objects.all()[:15]
        return render(request,'index.html',{
           'all_banners':all_banners,
           'course':course,
           'banner_courses':banner_courses,
           'courseorg':courseorg
        })




# 配置404
def page_not_found(request):
    from django.shortcuts import render_to_response
    response = render_to_response('404.html',{})
    response.status_code = 404
    return response


def page_error(request):
    from django.shortcuts import render_to_response
    response = render_to_response('500.html',{})
    response.status_code = 500
    return response
