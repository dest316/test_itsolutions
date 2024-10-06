from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter
from .views import CarViewSet, CommentViewSet


# Роутер, обеспечивающий корректную работу API, связанную с запросами о записях об автомобилях
router = DefaultRouter()
router.register('cars', CarViewSet)

# Представление для API, связанное с обработкой комментариев
comment_list = CommentViewSet.as_view({
    'get': 'list',
    'post': 'create',
})

urlpatterns = [
    path('', views.index, name='main_page'),
    path('users/', include('users.urls')),
    path('cars', views.your_cars_list, name='your_cars'),
    path('cars/add', views.add_car, name='add_car'),
    path('cars/edit/<int:pk>', views.UpdateCar.as_view(), name='edit_car'),
    path('cars/delete/<int:pk>', views.DeleteCar.as_view(), name='delete_car'),
    path('cars/<int:pk>', views.ViewCar.as_view(), name='show_car'),
    path('api/cars/<int:car_pk>/comments/', comment_list, name='car-comments'),
    path('api/', include(router.urls))
]
