from django.conf.urls import url
from scrunban.settings import base as base_settings
from . import views
from .project_views import flow, sprint, role, team

urlpatterns = [
    url(r'^(?P<project_id>[0-9]+)/$', views.index,
        name=base_settings.PROJECT_INDEX),
    url(r'^(?P<project_id>[0-9]+)/role/$', role.RoleListView.as_view(),
        name=base_settings.PROJECT_ROLE_LIST),
    url(r'^(?P<project_id>[0-9]+)/role/create/$', role.RoleCreateView.as_view(),
        name=base_settings.PROJECT_ROLE_CREATE),
    url(r'^(?P<project_id>[0-9]+)/role/edit/(?P<rol_id>[0-9]+)/$', role.RoleEditView.as_view(),
        name=base_settings.PROJECT_ROLE_EDIT),
    url(r'^(?P<project_id>[0-9]+)/role/delete/(?P<rol_id>[0-9]+)/$', role.RoleDeleteView.as_view(),
        name=base_settings.PROJECT_ROLE_DELETE),
    url(r'^(?P<project_id>[0-9]+)/dev/$', team.DevListView.as_view(),
        name=base_settings.PROJECT_DEV_LIST),
    url(r'^(?P<project_id>[0-9]+)/dev/edit/(?P<team_id>[0-9]+)/$', team.DevEditView.as_view(),
        name=base_settings.PROJECT_DEV_EDIT),
    url(r'^(?P<project_id>[0-9]+)/sprint/$', sprint.SprintListView.as_view(),
        name=base_settings.PROJECT_SPRINT_LIST),
    url(r'^(?P<project_id>[0-9]+)/sprint/create/$', sprint.SprintCreateView.as_view(),
        name=base_settings.PROJECT_SPRINT_CREATE),
    url(r'^(?P<project_id>[0-9]+)/sprint/edit/(?P<sprint_id>[0-9]+)/$', sprint.SprintEditView.as_view(),
        name=base_settings.PROJECT_SPRINT_EDIT),
    url(r'^(?P<project_id>[0-9]+)/sprint/delete/(?P<sprint_id>[0-9]+)/$', sprint.SprintDeleteView.as_view(),
        name=base_settings.PROJECT_SPRINT_DELETE),
    url(r'^(?P<project_id>[0-9]+)/sprint/detail/(?P<sprint_id>[0-9]+)/$', sprint.SprintDetailView.as_view(),
        name=base_settings.PROJECT_SPRINT_DETAIL),
    url(r'^(?P<project_id>[0-9]+)/flow/create/$', flow.FlowCreateView.as_view(),
        name=base_settings.PROJECT_FLOW_CREATE),
    url(r'^(?P<project_id>[0-9]+)/flow/$', flow.FlowListView.as_view(),
        name=base_settings.PROJECT_FLOW_LIST),
    url(r'^(?P<project_id>[0-9]+)/flow/edit/(?P<flow_id>[0-9]+)/$', flow.FlowEditView.as_view(),
        name=base_settings.PROJECT_FLOW_EDIT),
    url(r'^(?P<project_id>[0-9]+)/flow/delete/(?P<flow_id>[0-9]+)/$', flow.FlowDeleteView.as_view(),
        name=base_settings.PROJECT_FLOW_DELETE),
]

