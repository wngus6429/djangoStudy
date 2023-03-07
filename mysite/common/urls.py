from django.urls import path
from django.contrib.auth import views as auth_views

app_name = 'common'

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='common/login.html'), name='login'),
    # contrib.auth 앱의 LoginView 클래스를 활용해서 별도의 views.py 파일 수정 안해도 됨.
    # as_view 설정으로 registration디렉터리가 아닌 common 디렉터리에서 login.html파일을 참조한다.
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]