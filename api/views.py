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
    ]
    
    return Response(routes)

@api_view(["GET"])
def seeClassrooms(request):
    classrooms = Classroom.objects.all()
    classroomsSerialzed = ClassroomSerialzer(classrooms, many=True)

    return Response(classroomsSerialzed.data)
