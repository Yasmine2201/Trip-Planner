from django.shortcuts import render
from rest_framework.response import Response


def hello(request):
    return Response("Hello, world!")