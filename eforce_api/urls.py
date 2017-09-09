from django.conf.urls import url
from eforce_api import views

urlpatterns = [

    url(r'api/v1.0/crisis/case/new/$', views.CrisisCaseView.as_view(), name="crisis-case-new"),
    url(r'api/v1.0/crisis/case/(?P<pk>[0-9]+)/new/strategy/$', views.CrisisStrategyView.as_view(), name="crisis-case-new-strategy"),

]
