from django.urls import path, include
from . import views


urlpatterns = [
    path('reg', views.reg, name='reg'),
    path('auth', views.log_on, name='auth'),
    path('logout', views.log_out, name='logout')
]
