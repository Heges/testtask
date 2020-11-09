from . import views
from django.urls import path

from .views import UserProfileListCreateView, UserProfileDetailView, ServiceView, ServiceCreateView, PreviewMastersView

urlpatterns = [
    path('', views.MainIndexView.as_view(), name='index'),
    path('registration/', views.RegistrationUsersApi.as_view(), name='registration'),
    path('profile/', views.ProfileUserView.as_view(), name='profiles'),
    path("all-profiles/", UserProfileListCreateView.as_view(), name="all-profiles"),
    path("service/", ServiceView.as_view(), name="service"),
    path("service/create/", ServiceCreateView.as_view(), name="service_create"),
    path("masters/", PreviewMastersView.as_view(), name="masters_view"),

]