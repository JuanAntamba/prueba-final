from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    path('', views.home_quicku, name='home'),
    path('oferta/<int:promocion_id>/', views.detalle_oferta, name='detalle_oferta'),
    path('historial/', views.historial_consumo, name='historial'),
    path('notificacion/<int:notificacion_id>/descartar/', views.descartar_notificacion, name='descartar_notificacion'),
]