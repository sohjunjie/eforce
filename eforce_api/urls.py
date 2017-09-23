from django.conf.urls import url
from eforce_api import views

urlpatterns = [

    url(r'api/v1.0/crisis/case/new/$', views.CrisisCaseView.as_view(), name="crisis-case-new"),
    url(r'api/v1.0/crisis/case/(?P<pk>[0-9]+)/new/strategy/$', views.CrisisStrategyView.as_view(), name="crisis-case-new-strategy"),

    url(r'api/v1.0/crisis/case/(?P<pk>[0-9]+)/$', views.CrisisCaseDetailView.as_view(), name="crisis-case-view"),
    url(r'api/v1.0/crisis/unread/search/$', views.CrisisCaseUnreadSearchView.as_view(), name="crisis-case-search"),

    url(r'api/v1.0/crisis/case/(?P<pk>[0-9]+)/ef/update/$', views.CrisisUpdateListView.as_view(), name="crisis-case-ef-updates"),

    url(r'api/v1.0/user/group/(?P<pk>[0-9]+)/image/upload/$', views.UserGroupImageUploadView.as_view(), name="usergroup-image-upload")

]
