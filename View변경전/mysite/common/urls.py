from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

app_name = 'common'

urlpatterns = [
    # contrib.auth 앱의 LoginView 클래스를 활용해서 별도의 views.py 파일 수정 안해도 됨.
    # as_view 설정으로 registration디렉터리가 아닌 common 디렉터리에서 login.html파일을 참조한다.
    path('login/', auth_views.LoginView.as_view(template_name='common/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('signup/', views.signup, name='signup'),
    # 이로인해 로그인 화면에서 회원가입 링크 누르면 이게 실행
]