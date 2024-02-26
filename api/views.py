from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from base.models import *
from .serializers import *

# Create your views here.
@api_view(['GET'])
def routing(request):
    routes = [
        "/api",
        "/api/classrooms",
        "/api/classrooms/:id",
        "/api/users",
        "/ap/users/:id",
        "/api/classrooms/users/:id"
    ]
    
    return Response(routes)

@api_view(["GET"])
def seeClassrooms(request):
    classrooms = Classroom.objects.all()
    classroomsSerialzed = ClassroomSerialzer(classrooms, many=True)

    return Response(classroomsSerialzed.data)

@api_view(["GET"])
def seeClassroom(request, pk):
    classroom = Classroom.objects.get(id=pk)
    classroomSerialzed = ClassroomSerialzer(classroom, many=False)
    
    return Response(classroomSerialzed.data)

@api_view(["GET"])
def seeUsers(request):
    return Response(UserSerialzer(User.objects.all(), many=True).data)

@api_view(['GET'])
def seeUser(request, pk):
    user = UserSerialzer(User.objects.get(id=pk), many=False)
    return Response(user.data)

@api_view(["GET"])
def seeUserClassrooms(request, pk):
    user = User.objects.get(id=pk)
    userClassrooms = user.classroom_set.all() #All classrooms created by user, not the ones they joined
    
    classroomsSerialzed = ClassroomSerialzer(userClassrooms, many=True)
    return Response(classroomsSerialzed.data)