from django.urls import path
from . import views

urlpatterns = [
    path('add-expense/', views.ExpenseCreateView.as_view(), name="add-expense"),

    path('<str:pk>/', views.GroupDetailView.as_view(), name="detail"),
]