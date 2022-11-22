from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path('', views.Hub.as_view(), name='hub'),
    path('update/', views.ProfileUpdate.as_view(), name='profile-update'),
    path('delete/', views.profile_delete, name="profile-delete"),
    path('opportunities/', views.Opportunities.as_view(), name='opportunities'),
    path('opportunities/<int:pk>', views.opportunities_apply, name='opportunity-detail'),
    path('materials/', views.Materials.as_view(), name='materials'),
    path('post/', views.PostList.as_view(), name='post'),
    path('post/<slug:slug>/', views.PostDetail.as_view(), name='post_detail'),
    path('proposals/', views.Proposals.as_view(), name='proposals'),
    path('proposals/<int:pk>', views.proposals_apply, name='proposal-apply'),
    path('proposals/submit', views.ProposalCreateView.as_view(), name='proposal-create'),
    path('proposals/manage', views.ProposalsManage.as_view(), name='proposal-manage'),
    path('proposals/manage/switch/<int:pk>', views.proposal_switch, name='proposal-switch'),
    path('proposals/manage/delete/<int:pk>', views.proposal_delete, name='proposal-delete'),
    path('proposals/manage/applicants/<int:pk>', views.ProposalApplicantsView.as_view(), name='proposal-applicants'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
