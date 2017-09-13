from django.conf.urls import url
from eforce_front import views

urlpatterns = [

    url(r'^(?i)$', views.go_to_signin, name="ef-signin"),
    url(r'^(?i)home/$', views.go_to_homepage, name="ef-home"),
    url(r'^(?i)home/logout/$', views.logout_user, name="ef-home-logout"),

]
