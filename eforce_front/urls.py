from django.conf.urls import url
from eforce_front import views

urlpatterns = [

    url(r'^(?i)$', views.go_to_signin, name="signin"),
    url(r'^(?i)home/$', views.go_to_homepage, name="home"),
    url(r'^(?i)home/logout/$', views.logout_user, name="logout"),

    url(r'^(?i)hq/dispatch/ef/$', views.go_to_dispatch_ef_page, name="hq-dispatch-ef"),
    url(r'^(?i)hq/crisis/manage/$', views.go_to_manage_crisis_page, name="hq-manage-crisis"),
    url(r'^(?i)hq/update/cmo/$', views.go_to_update_cmo_page, name="hq-update-cmo"),
    url(r'^(?i)hq/view/sent/update/$', views.go_to_efhq_view_sent_update_page, name="hq-sent-updates"),

    url(r'^(?i)efassets/update/hq/$', views.go_to_update_hq_page, name="assets-update-hq"),
    url(r'^(?i)efassets/view/sent/update/$', views.go_to_efassets_view_sent_update_page, name="assets-sent-updates"),

]
