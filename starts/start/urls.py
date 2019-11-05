"""start URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
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
from django.conf.urls import url, include
from django.contrib import admin
from rest_framework_swagger.views import get_swagger_view
from hupu.views import *

schema_view = get_swagger_view(title='Pastebin API')

urlpatterns = [
    url(r'^$', schema_view),
    url(r'^admin/', admin.site.urls),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'new/$', SourceNewViewSet.as_view()),
    url(r'detail/(?P<pk>[0-9]+)$', SourceGetViewSet.as_view()),
    url(r'details/$', SourceListViewSet.as_view()),
    # url(r'bulk_update/$', SourceBulkUpdateViewSet.as_view()),
    url(r'bulk_update/$', bulkUpdate),
    url(r'update/(?P<pk>[0-9]+)$', SourceSingleUpdateViewSet.as_view()),
]

