from django.urls import path,include,re_path
from .views import UserInfoView,ImageUploadView,ChangePwdView
app_name = 'users'
urlpatterns = [
    # 用户信息
    path('info/',UserInfoView.as_view(),name="user_info"),
    # 用户头像上传
    path('image/upload/',ImageUploadView.as_view(),name="image_upload"),
    #
    path('update/pwd/',ChangePwdView.as_view(),name="update_pwd"),






]
