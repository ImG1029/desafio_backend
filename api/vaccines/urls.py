from django.urls import path
from api.vaccines.views import VaccineListCreateView, VaccineDetailView

urlpatterns = [
    path("", VaccineListCreateView.as_view()),
    path("<int:pk>/", VaccineDetailView.as_view()),
]