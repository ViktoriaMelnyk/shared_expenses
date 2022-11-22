from django.urls import path
from . import views

urlpatterns = [
    path('add-expense/', views.ExpenseCreateView.as_view(), name="add-expense"),
    path('expense/<str:pk>/', views.ExpenseUpdateView.as_view(), name="expense"),
    path('expense/<str:pk>/delete', views.ExpenseDeleteView.as_view(), name="delete-expense"),
    path('settle-up/', views.SettleUpView.as_view(), name="settle-up"),

    path('create/', views.GroupCreateView.as_view(), name="create"),
    path('<str:pk>/', views.GroupDetailView.as_view(), name="detail"),
    path('<str:pk>/delete', views.GroupDeleteView.as_view(), name="delete"),
    path('<str:pk>/edit', views.GroupUpdateView.as_view(), name="edit"),
    path('<str:pk>/join', views.GroupInvite.as_view(), name="join"),
]