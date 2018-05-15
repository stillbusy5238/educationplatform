from django.urls import path,include,re_path
from .views import UserInfoView,ImageUploadView,ChangePwdView,SendEmailView,UpdateEmailView,MyCourseView,MyFavOrgView
from .views import MyFavTeacherView,MyFavCourseView,MyMessageView
app_name = 'users'
urlpatterns = [
    # 用户信息
    path('info/',UserInfoView.as_view(),name="user_info"),
    # 用户头像上传
    path('image/upload/',ImageUploadView.as_view(),name="image_upload"),
    #
    path('update/pwd/',ChangePwdView.as_view(),name="update_pwd"),
    # 发送邮箱验证码
    path('sendemail_code/',SendEmailView.as_view(),name="sendemail_code"),
    # 修改邮箱
    path('update_email/',UpdateEmailView.as_view(),name="update_email"),
    # 个人课程
    path('mycourse/',MyCourseView.as_view(),name="mycourse"),
    # 个人收藏机构
    path('myfav/org',MyFavOrgView.as_view(),name="myfav_org"),
    # 个人收藏教师
    path('myfav/teacher',MyFavTeacherView.as_view(),name="myfav_teacher"),
    # 个人收藏课程
    path('myfav/course',MyFavCourseView.as_view(),name="myfav_course"),
    # 个人消息
    path('mymessage/',MyMessageView.as_view(),name="mymessage"),





]
