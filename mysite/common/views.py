from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from .forms import UserForm

def signup(request):
    """
    계정생성
    """
    # POST요청인 경우 입력한 데이터로 새로운 사용자를 생성하고
    # GET 요청인 경우 common/singup.html 화면을 반환한다.
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            # cleaned_data_get은 입력한 값을 얻기위해 사용하는 함수이다.
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('index')
    else:
    # GET요청
        print("왓네")
        form = UserForm()
    return render(request, 'common/signup.html', {'form': form})
