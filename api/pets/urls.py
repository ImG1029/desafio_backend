from django.urls import path
from .views import PetListCreateView, PetDetailView

urlpatterns = [
    path("", PetListCreateView.as_view()),
    path("<int:pet_id>/", PetDetailView.as_view())
]