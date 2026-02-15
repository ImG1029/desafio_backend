from django.urls import path
from .views import VaccinationRecordListCreateView, VaccinationRecordDetailView

urlpatterns = [
    path("", VaccinationRecordListCreateView.as_view()),
    path("<int:pk>/", VaccinationRecordDetailView.as_view())
]