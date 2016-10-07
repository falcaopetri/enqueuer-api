from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns
from api import views

urlpatterns = [
    url(r'^$', views.api_root),
    url(r'^friendship/', include('friendship.urls')),
]

urlpatterns = format_suffix_patterns(urlpatterns)
