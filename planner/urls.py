from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'phases', views.PhaseViewSet)

urlpatterns = [
    path('', views.index, name='index'),
    path('api/', include(router.urls)),
    path('api/phases/<int:phase_id>/notes/', views.NoteViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('api/phases/<int:phase_id>/notes/<int:pk>/', views.NoteViewSet.as_view({'get': 'retrieve', 'delete': 'destroy'})),
] 