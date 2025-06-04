from django.shortcuts import render
from django.http import HttpResponse


def dialogue(request):
    return HttpResponse("Hello, Django!")
