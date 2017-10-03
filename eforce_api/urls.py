from django.conf.urls import url
from eforce_api import views

urlpatterns = [

    url(r'api/v1.0/crisis/case/new/$', views.CrisisCaseView.as_view(), name="crisis-case-new"),
    url(r'api/v1.0/crisis/case/(?P<pk>[0-9]+)/new/strategy/$', views.CrisisStrategyView.as_view(), name="crisis-case-new-strategy"),

    url(r'api/v1.0/crisis/case/(?P<pk>[0-9]+)/$', views.CrisisCaseDetailView.as_view(), name="crisis-case-view"),
    url(r'api/v1.0/crisis/unresolved/search/$', views.CrisisCaseUnresolvedSearchView.as_view(), name="crisis-case-unresolved-search"),

    url(r'api/v1.0/crisis/case/(?P<pk>[0-9]+)/strategy/$', views.CrisisCombatStrategyListView.as_view(), name="crisis-case-combat-strategy"),
    url(r'api/v1.0/crisis/case/(?P<pk>[0-9]+)/ef/update/$', views.CrisisUpdateListView.as_view(), name="crisis-case-ef-updates"),
    url(r'api/v1.0/crisis/case/(?P<pk>[0-9]+)/ef/group/instruction/$', views.CrisisInstructionListView.as_view(), name="crisis-case-group-instruction"),

    url(r'api/v1.0/user/group/(?P<pk>[0-9]+)/image/upload/$', views.UserGroupImageUploadView.as_view(), name="usergroup-image-upload"),
    url(r'api/v1.0/user/group/search/$', views.EFAssetsGroupListView.as_view(), name="user-group-list"),

    url(r'api/v1.0/this/user/group/$', views.ThisUserGroupRoleView.as_view(), name="this-user-group"),

    url(r'api/v1.0/crisis/(?P<pk>[0-9]+)/mark/read/$', views.MarkAsReadCMOCrisisCase.as_view(), name="mark-crisis-read"),
    url(r'api/v1.0/instruction/(?P<pk>[0-9]+)/mark/read/$', views.MarkAsReadCrisisInstruction.as_view(), name="mark-instruction-read"),

    url(r'api/v1.0/strategy/(?P<pk>[0-9]+)/mark/read/$', views.MarkAsReadCombatStrategy.as_view(), name="mark-combat-strategy-read"),
    url(r'api/v1.0/efassets/update/(?P<pk>[0-9]+)/mark/read/$', views.MarkAsReadEFAssetsUpdate.as_view(), name="mark-efassets-update-read"),

]
