from django.db import models
from datetime import datetime
from organization.models import CourseOrg,Teacher
# Create your models here.


class Course(models.Model):
    name = models.CharField(max_length=50,verbose_name= u"课程名")
    desc = models.CharField(max_length=300,verbose_name= u"课程描述")
    detail =models.TextField(verbose_name= u"课程详情")
    is_banner = models.BooleanField(default=False,verbose_name="是否轮播")
    degree = models.CharField(choices= (("easy","初级"),("medium","中级"),("hard","高级")),max_length=10)
    learn_times = models.IntegerField(default=0,verbose_name= u"学习时长(分钟数)")
    students = models.IntegerField(default=0,verbose_name = u"学习人数")
    fav_nums = models.IntegerField(default=0,verbose_name = u"收藏")
    image = models.ImageField(upload_to="courses/%Y/%m",verbose_name=u"封面图",max_length=100)
    click_nums = models.IntegerField(default=0,verbose_name=u"点击数")
    category = models.CharField(max_length=50,verbose_name= u"课程类别", default="后端开发")
    tag = models.CharField(default="",verbose_name="课程标签",max_length=10)
    teacher = models.ForeignKey(Teacher,verbose_name="讲师",null=True,blank="True",on_delete=models.CASCADE)
    course_org = models.ForeignKey(CourseOrg,verbose_name=u"所属机构",on_delete=models.CASCADE,null=True,blank=True)
    youneed_know = models.CharField(max_length=300,verbose_name="课程须知",default="")
    teacher_tell = models.CharField(max_length=300,verbose_name="老师告诉你",default="")
    add_time = models.DateTimeField(default= datetime.now,verbose_name= u"添加时间")

    class Meta:
        verbose_name = u"课程"
        verbose_name_plural = verbose_name
    def get_zj_nums(self):
        # 获取章节数
        all_lessons = self.lesson_set.all().count()
        return all_lessons

    def get_learn_nums(self):
        # 获取章节数
        return self.usercourse_set.all()[:5]
    def get_course_lessons(self):
        # 获取课程所有章节
        return self.lesson_set.all()


    def __str__(self):
        return self.name


# 一个课程会有多个章节 用外间完成
class Lesson(models.Model):
    course = models.ForeignKey(Course,verbose_name= u"课程",on_delete=models.CASCADE)
    name = models.CharField(max_length=100,verbose_name= u"章节名")
    add_time=models.DateTimeField(default= datetime.now,verbose_name= u"添加时间")

    class Meta:
        verbose_name = u"章节"
        verbose_name_plural = verbose_name

    def get_lesson_video(self):
        # 获取章节视频
        return self.video_set.all()
    def __str__(self):
        return self.name


class Video(models.Model):
    lesson = models.ForeignKey(Lesson,verbose_name= u"章节",on_delete=models.CASCADE)
    name = models.CharField(max_length=100,verbose_name= u"视频名")
    url = models.CharField(max_length=200,verbose_name="访问地址",default="")
    learn_times = models.IntegerField(default=0,verbose_name= u"学习时长(分钟数)")
    add_time=models.DateTimeField(default= datetime.now,verbose_name= u"添加时间")

    class Meta:
        verbose_name = u"视频"
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.name






class CourseResource(models.Model):

    course = models.ForeignKey(Course,verbose_name= u"课程",on_delete=models.CASCADE)
    name = models.CharField(max_length=100,verbose_name= u"名称")
    download = models.FileField(upload_to="courses/resource/%Y/%m",verbose_name= u"资源文件",max_length=100)

    add_time=models.DateTimeField(default= datetime.now,verbose_name= u"添加时间")

    class Meta:
        verbose_name = u"资源信息"
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.name
