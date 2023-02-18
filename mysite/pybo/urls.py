from django.urls import path
from . import views

urlpatterns = [
    # views 파일 안에 index 함수를 참조 한다고
    path('', views.index)
]