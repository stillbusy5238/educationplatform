from django.urls import path,include,re_path
from .views import CourseListView,CourseDetailView
app_name = 'courses'
urlpatterns = [
    path('list/',CourseListView.as_view(),name="course_list"),
    re_path('detail/(?P<course_id>\d+)',CourseDetailView.as_view(),name="course_detail")

]
