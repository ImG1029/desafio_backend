from django.urls import path, include
from .views import HealthView

urlpatterns = [
    path('health/', HealthView.as_view()),
    path('owners/', include('api.owners.urls')),
    path('pets/', include('api.pets.urls')),
]