from django.conf.urls import url
from eforce_front import views

urlpatterns = [

    url(r'^(?i)$', views.go_to_signin, name="ef-signin"),
    url(r'^(?i)home/$', views.go_to_homepage, name="ef-home"),
    url(r'^(?i)home/logout/$', views.logout_user, name="ef-logout"),

    url(r'^(?i)efassets/manage/$', views.go_to_manage_ef_assets_page, name="ef-efassets-manage"),

]
