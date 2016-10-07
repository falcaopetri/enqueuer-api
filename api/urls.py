from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns
from api import views

urlpatterns = [
    url(r'^friendship/', include('friendship.urls')),
    url(r'^user/', views.UserList.as_view()),
    url(r'^queue/', views.QueueList.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
