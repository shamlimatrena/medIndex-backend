from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MedViewSet
from .views import LoginView

router = DefaultRouter()
router.register(r'meds', MedViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('login/', LoginView.as_view(), name='login'),
]
