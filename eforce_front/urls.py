from django.conf.urls import url
from eforce_front import views

urlpatterns = [

    url(r'^(?i)$', views.index, name="ef-index"),
    url(r'^(?i)home/$', views.homepage, name="ef-home"),

]
