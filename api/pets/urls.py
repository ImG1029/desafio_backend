from django.urls import path
from .views import PetListCreateView, PetDetailView

urlpatterns = [
    path("", PetListCreateView.as_view()),
    path("<int:pk>/", PetDetailView.as_view())
]