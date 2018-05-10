from django.urls import path,include,re_path
from organization.views import OrgView,AddUserAskView

app_name = 'org'
urlpatterns = [
    # 机构列表
    path('list/',OrgView.as_view(),name="org_list"),
    path('add_ask/',AddUserAskView.as_view(),name="add_ask")
]
