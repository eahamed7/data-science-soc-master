from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView


from home import views

app_name = 'home'
urlpatterns = [
    path('', views.index, name='index'),
    path('sponsorship', TemplateView.as_view(template_name='home/sponsorship.html'), name='sponsorship'),
    path('flagships', TemplateView.as_view(template_name='home/flagships.html'), name='flagships'),
    path('freshers', views.freshers, name='freshers'),
    path('404', TemplateView.as_view(template_name='home/404.html'), name='404'),
    path('privacy-notice', TemplateView.as_view(template_name='home/privacy-notice.html'), name='privacy_notice'),
    path('terms-and-conditions', TemplateView.as_view(template_name='home/terms-and-conditions.html'), name='terms_and_conditions'),
    ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)