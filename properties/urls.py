from django.urls import path
from . import views

urlpatterns = [
    path("", views.property_list, name="properties"),
]
