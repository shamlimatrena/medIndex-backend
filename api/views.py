from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse

def ping(request):
    return JsonResponse({"message": "pong"})


def say_hello(request):
    return render(request, 'hello.html', { 'name': 'Trena'} )
