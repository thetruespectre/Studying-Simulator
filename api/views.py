from django.shortcuts import render
from django.http import JsonResponse

# Create your views here.
def routing(request):
    urls = [
        'sdas',
        'POST /api/classrooms'
        'GET /api/classrooms/:id'
        
        'GET /api/users/'
        'GET /api/users/:id'
    ]
    
    return JsonResponse(urls, safe=False)