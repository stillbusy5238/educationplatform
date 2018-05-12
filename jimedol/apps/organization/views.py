from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponse
from .models import CourseOrg,CityDict,Teacher
from .forms import UserAskForm
from courses.models import Course
from operation.models import UserFavorite
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
# Create your views here.
class OrgView(View):
    # 课程机构列表
    def get(self,request):
        # 课程机构
        all_orgs = CourseOrg.objects.all()
        hot_orgs = all_orgs.order_by("click_nums")[:3]
        # 城市
        all_cities = CityDict.objects.all()
        # 取出筛选城市
        city_id = request.GET.get('city', "")
        if city_id:
            all_orgs = all_orgs.filter(city_id=int(city_id))
        # 类别筛选
        category = request.GET.get('ct', "")
        if category:
            all_orgs = all_orgs.filter(category = category)
        sort = request.GET.get('sort', "")
        if sort:
            if sort == "students":
                all_orgs = all_orgs.order_by("-students")
            elif sort == "courses":
                all_orgs = all_orgs.order_by("-course_nums")
        org_nums = all_orgs.count()
        # 做分页
        try:
           page = request.GET.get('page', 1)
        except PageNotAnInteger:
           page = 1



    # Provide Paginator with the request object for complete querystring generation

        p = Paginator(all_orgs, 5, request=request)

        orgs = p.page(page)
        return render(request,"org-list.html",{
          "all_orgs" : orgs,
          "all_cities": all_cities,
          "org_nums": org_nums,
          "city_id":city_id,
          "category" : category,
          "hot_orgs":hot_orgs,
          "sort":sort

        })


class AddUserAskView(View):
    # 用户添加咨询
    def post(self,request):
        userask_form = UserAskForm(request.POST)
        if userask_form.is_valid():

            user_ask = userask_form.save(commit=True)
            # 返回
            return HttpResponse('{"status":"success"}',content_type='application/json')
        else:
            return HttpResponse('{"status":"fail", "msg":"添加出错"}', content_type='application/json')



class OrgHomeView(View):
    def get(self,request,org_id):
        current_page = "home"

        course_org = CourseOrg.objects.get(id = int(org_id))
        has_fav =False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id,fav_type=2):
                has_fav = True



        all_courses = course_org.course_set.all()[:3]

        all_teachers = course_org.teacher_set.all()[:1]
        return render(request,'org-detail-homepage.html',{
          'all_courses':all_courses,
          'all_teachers':all_teachers,
          'course_org':course_org,
          'current_page':current_page,
          'has_fav':has_fav
        })


class OrgCourseView(View):
    def get(self,request,org_id):
        current_page = "course"
        course_org = CourseOrg.objects.get(id = int(org_id))
        all_courses = course_org.course_set.all()
        has_fav =False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id,fav_type=2):
                has_fav = True


        return render(request,'org-detail-course.html',{
          'all_courses':all_courses,

          'course_org':course_org,
          'current_page':current_page,
          'has_fav':has_fav
        })


class OrgDescView(View):
    def get(self,request,org_id):
        current_page = "desc"
        course_org = CourseOrg.objects.get(id = int(org_id))
        has_fav =False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id,fav_type=2):
                has_fav = True



        return render(request,'org-detail-desc.html',{


          'course_org':course_org,
          'current_page':current_page,
          'has_fav':has_fav
        })

class OrgTeacherView(View):
    def get(self,request,org_id):
        current_page = "teacher"
        course_org = CourseOrg.objects.get(id = int(org_id))


        all_teachers = course_org.teacher_set.all()
        has_fav =False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id,fav_type=2):
                has_fav = True
        return render(request,'org-detail-teachers.html',{

          'all_teachers':all_teachers,
          'course_org':course_org,
          'current_page':current_page,
          'has_fav':has_fav
        })


class AddFavView(View):
    # 用户收藏,取消收藏
    def post(self,request):
        fav_id = request.POST.get('fav_id',0)
        fav_type = request.POST.get('fav_type',0)

        if not request.user.is_authenticated:
            # 判断用户登录状态
            return HttpResponse('{"status":"fail", "msg":"用户未登录"}', content_type='application/json')


        exist_records = UserFavorite.objects.filter(user=request.user, fav_id=int(fav_id),fav_type=fav_type)
        if exist_records:
            # 已经存在，责表示用户取消收藏
            exist_records.delete()
            return HttpResponse('{"status":"success", "msg":"收藏"}', content_type='application/json')
        else:
            user_fav = UserFavorite()
            if int(fav_id)>0 and int(fav_type) > 0:
               user_fav.user = request.user
               user_fav.fav_id = int(fav_id)
               user_fav.fav_type = int(fav_type)
               user_fav.save()
               return HttpResponse('{"status":"success", "msg":"已收藏"}', content_type='application/json')
            else:
               return HttpResponse('{"status":"fail", "msg":"收藏出错"}', content_type='application/json')


class TeacherListView(View):
    # 课程讲师列表页
    def get(self,request):
        all_teachers = Teacher.objects.all()
        sort = request.GET.get('sort', "")
        if sort:
            if sort == "hot":
                all_teachers = all_teachers.order_by("-click_nums")
        sorted_teacher = Teacher.objects.all().order_by("-click_nums")[:3]

        # 做分页
        try:
           page = request.GET.get('page', 1)
        except PageNotAnInteger:
           page = 1



    # Provide Paginator with the request object for complete querystring generation

        p = Paginator(all_teachers, 1, request=request)

        teachers = p.page(page)

        return render(request,"teachers-list.html",{
           'all_teachers':teachers,
           'sort':sort,
           'sorted_teacher':sorted_teacher
        })
