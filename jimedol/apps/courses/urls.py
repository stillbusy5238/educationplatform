from django.urls import path,include,re_path
from .views import CourseListView,CourseDetailView,CourseInfoView,CommentView,AddCommentsView,VideoPlayView
app_name = 'courses'
urlpatterns = [
    path('list/',CourseListView.as_view(),name="course_list"),
    re_path('detail/(?P<course_id>\d+)',CourseDetailView.as_view(),name="course_detail"),
    re_path('info/(?P<course_id>\d+)',CourseInfoView.as_view(),name="course_video"),
    # 课程评论
    re_path('comment/(?P<course_id>\d+)',CommentView.as_view(),name="course_comment"),
    # 添加课程评论
    path('add_comment/',AddCommentsView.as_view(),name="add_comment"),
    re_path('video/(?P<video_id>\d+)',VideoPlayView.as_view(),name="video_play"),



]
