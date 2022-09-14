from django.urls import path
from . import views

urlpatterns = [
    path('<str:pk>/', views.GroupDetailView.as_view(), name="detail"),
]