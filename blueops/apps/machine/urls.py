from django.conf.urls import url
from .views import list,sysinfo,lanxi,collectSysInfoHandler,collectPackageHandler

urlpatterns = [
    url(r'^list/$', list, name='list'),  # 首页
    url(r'^list/(?P<page>\d+)/$', list, name='list'), # 首页
    url(r'^sysinfo/(?P<machine_id>.*)/$', sysinfo, name='sysinfo'), # 系统页
    url(r'^lanxi/(?P<machine_id>.*)/$', lanxi, name='lanxi'), # lanxi页
    url(r'^collectsysinfo/$',collectSysInfoHandler),
    url(r'^collectpackage/$',collectPackageHandler)
]
