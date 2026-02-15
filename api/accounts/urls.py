from django.urls import path

from api.accounts.views import AccountListCreateView, AccountDetailView, LoginView

urlpatterns = [
    path("", AccountListCreateView.as_view()),
    path("<int:pk>/", AccountDetailView.as_view()),
    path('login/', LoginView.as_view(), name='login'),
]