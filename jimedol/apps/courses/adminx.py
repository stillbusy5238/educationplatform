import xadmin
from .models import Course,BannerCourse
from .models import Lesson
from .models import Video
from .models import CourseResource
from organization.models import CourseOrg



class LessonInline(object):
    model = Lesson
    extra = 0

class CourseAdmin(object):

    list_display = ['name','desc','detail','degree','learn_times','students']
    search_fields = ['name','desc','detail','degree','students']
    list_filter =['name','desc','detail','degree','learn_times','students']
    ordering = ['-students']
    readonly_fields = ['students']
    # list_editable直接在列表页编辑
    # refresh_times=[3,5]定时刷新
    # 不显示
    # exclude = []
    #课程嵌套
    inlines = [LessonInline]

    # 每次统计
    def save_models(self):
        # 在保存课程的时候统计课程机构的课程数
        obj = self.new_obj
        obj.save()
        if obj.course.org is not None:

            course_org = obj.course_org
            course_org.course_nums = Course.objects.filter(course_org=course_org).count()
            course_org.save()


class BannerCourseAdmin(object):
        list_display = ['name','desc','detail','degree','learn_times','students']
        search_fields = ['name','desc','detail','degree','students']
        list_filter =['name','desc','detail','degree','learn_times','students']
        ordering = ['-students']
        readonly_fields = ['students']
        # 不显示
        # exclude = []
        #课程嵌套
        inlines = [LessonInline]

        def queryset(self):
            qs = super(BannerCourseAdmin,self).queryset()
            qs = qs.filter(is_banner=True)
            return qs


class LessonAdmin(object):
    list_display = ['course','name','add_time']
    search_fields = ['course','name']
    list_filter =['course__name','name','add_time']


class VideoAdmin(object):
    list_display = ['lesson','name','add_time']
    search_fields = ['lesson','name']
    list_filter =['lesson__name','name','add_time']

class CourseResourceAdmin(object):
    list_display = ['course','name','add_time','download']
    search_fields = ['course','name','download']
    list_filter =['course__name','name','add_time','download']
xadmin.site.register(Course,CourseAdmin)
xadmin.site.register(BannerCourse,BannerCourseAdmin)
xadmin.site.register(Lesson,LessonAdmin)
xadmin.site.register(Video,VideoAdmin)
xadmin.site.register(CourseResource,CourseResourceAdmin)
