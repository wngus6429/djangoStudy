from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse

def index(request):
    return HttpResponse('pybo에 온걸 환영합니다 주현님.')