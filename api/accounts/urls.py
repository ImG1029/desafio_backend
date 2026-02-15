from django.urls import path

from api.accounts.views import AccountListCreateView, AccountDetailView

urlpatterns = [
    path("", AccountListCreateView.as_view()),
    path("<int:pk>/", AccountDetailView.as_view()),
]