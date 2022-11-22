from django.urls import path
from django.urls import re_path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path('signup/', views.SignUp.as_view(), name='signup'),
    re_path(
        r'^course-autocomplete/$',
        views.CourseAutoComplete.as_view(),
        name='course-autocomplete',
    ),


]
