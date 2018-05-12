from django.urls import path,include,re_path
from organization.views import OrgView,AddUserAskView,OrgHomeView,OrgCourseView,OrgDescView,OrgTeacherView,AddFavView,TeacherListView,TeacherDetailView

app_name = 'org'
urlpatterns = [
    # 机构列表
    path('list/',OrgView.as_view(),name="org_list"),
    path('add_ask/',AddUserAskView.as_view(),name="add_ask"),
    re_path('home/(?P<org_id>\d+)',OrgHomeView.as_view(),name="org_homepage"),
    re_path('course/(?P<org_id>\d+)',OrgCourseView.as_view(),name="org_course"),
    re_path('desc/(?P<org_id>\d+)',OrgDescView.as_view(),name="org_desc"),
    re_path('teacher/(?P<org_id>\d+)',OrgTeacherView.as_view(),name="org_teacher"),

    # 机构收藏
    path('add_fav/',AddFavView.as_view(),name="add_fav"),
    # 讲师的列表页
    path('teacher/list/',TeacherListView.as_view(),name="teacher_list"),
    # 讲师详情
    re_path('teacher/detail/(?P<teacher_id>\d+)',TeacherDetailView.as_view(),name="teacher_detail")
]
