import xadmin
from .models import CityDict
from .models import CourseOrg
from .models import Teacher



class CityDictAdmin(object):
    list_display = ['name','desc','add_time']
    search_fields = ['name','desc']
    list_filter =['name','desc','add_time']


class CourseOrgAdmin(object):
    list_display = ['name','desc','add_time','address']
    search_fields = ['name','desc','address']
    list_filter =['name','desc','add_time','address']
    relfield_style = 'fk-ajax'


class TeacherAdmin(object):
    list_display = ['org','name','work_years','work_company']
    search_fields = ['org','name','work_years','work_company']
    list_filter =['org__name','name','work_years','work_company']
xadmin.site.register(CityDict,CityDictAdmin)
xadmin.site.register(CourseOrg,CourseOrgAdmin)
xadmin.site.register(Teacher,TeacherAdmin)
