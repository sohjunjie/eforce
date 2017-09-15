from django.conf.urls import url
from eforce_front import views

urlpatterns = [

    url(r'^(?i)$', views.go_to_signin, name="signin"),
    url(r'^(?i)home/$', views.go_to_homepage, name="home"),
    url(r'^(?i)home/logout/$', views.logout_user, name="logout"),

    url(r'^(?i)dispatch/ef/$', views.go_to_dispatch_ef_page, name="hq-dispatch-ef"),
    url(r'^(?i)crisis/manage/$', views.go_to_manage_crisis_page, name="hq-manage-crisis"),

    url(r'^(?i)update/hq/$', views.go_to_update_hq_page, name="assets-update-hq"),


]
