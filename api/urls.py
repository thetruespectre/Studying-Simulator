from django.urls import path
from . import views

urlpatterns = [
    path('', views.routing, name="see-routing"),
    path("classrooms/", views.seeClassrooms, name="see-classrooms"),
    path("classrooms/<int:pk>/", views.seeClassroom, name="see-classroom"),
    
    path("users/", views.seeUsers, name="see-users"),
    path("users/<int:pk>/", views.seeUser, name="see-user"),
    path("classrooms/users/<int:pk>/", views.seeUserClassrooms, name="see-user-classrooms")
]
