import xadmin
from xadmin import views
from .models import EmailVerifyRecord
from .models import Banner

class EmailVerifyRecordAdmin(object):

    list_display = ['code','email','send_type','send_time']
    search_fields = ['code','email','send_type']
    list_filter =['code','email','send_type','send_time']



class BannerAdmin(object):
    list_display = ['title','image','url','index','add_time']
    search_fields = ['title','image','url','index']
    list_filter =['title','image','url','index','add_time']

xadmin.site.register(EmailVerifyRecord,EmailVerifyRecordAdmin)
xadmin.site.register(Banner,BannerAdmin)

# 全站的配置放在这里
class BaseSetting(object):
    enable_themes = True

    use_bootswatch = True

xadmin.site.register(views.BaseAdminView,BaseSetting)


class GlobalSettings(object):
    site_title = 'jimedol管理系统'
    site_footer = 'jimedol'
    menu_style = 'accordion'
xadmin.site.register(views.CommAdminView,GlobalSettings)
