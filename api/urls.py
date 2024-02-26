from django.urls import path
from . import views

urlpatterns = [
    path('', views.routing, name="see-routing"),
    path("classrooms/", views.seeClassrooms, name="see-classrooms")
]
