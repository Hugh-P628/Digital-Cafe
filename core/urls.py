from django.urls import path

# This . package just means "the current package; we are importing the sister file "views.py"
from . import views

urlpatterns = [
    path("", views.index, name="index"),
]
