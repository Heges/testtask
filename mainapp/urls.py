from . import views
from django.urls import path

urlpatterns = [
    path('', views.MainIndexView.as_view(), name='index'),
    path('registration/', views.RegistrationUsersApi.as_view(), name='registration')
]