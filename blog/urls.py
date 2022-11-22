from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView


from blog import views

urlpatterns = [
    path('', views.Blog.as_view(), name='blog')
    ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)