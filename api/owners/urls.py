from django.urls import path
from .views import OwnerListCreateView, OwnerDetailView

urlpatterns = [
    path("", OwnerListCreateView.as_view()),
    path("<int:owner_id>/", OwnerDetailView.as_view())
]