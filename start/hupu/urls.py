from django.conf.urls import url, include
from hupu.views import *


urlpatterns = [
    url(r'^update/$', bulkUpdate),
    # url(r'^sourceUpdate/$', SourceUpdateViewSet.as_view()),
    # url(r'^sourceCreate/$', SourceCreateViewSet.as_view()),
]
