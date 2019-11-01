from django.conf.urls import url, include
from users.views import *


urlpatterns = [
    url(r'register/$', RegisterUserView.as_view()),
    url(r'login/$', LoginUserView.as_view()),
    url(r'logout/$', LoginOutUserView.as_view()),
    url(r'detail/$', DetailsUserView.as_view()),
]
