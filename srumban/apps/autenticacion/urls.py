"""srumban URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from srumban.settings import base as base_settings
from apps.autenticacion import views

urlpatterns = [
    url(r'^$', views.login, name=base_settings.LOGIN_NAME),
    url(r'^authenticate_user/$', views.authenticate_user, name=base_settings.AUTH_NAME),
    url(r'^deauthenticate_user/$', views.deauthenticate_user, name=base_settings.DEAUTH_NAME),
    
    url(r'^app/$', views.app, name=base_settings.APP_NAME), 
    url(r'^app2/$', views.app2, name=base_settings.APP2_NAME),
    url(r'^data/$', views.data, name=base_settings.DATA_NAME),
]
