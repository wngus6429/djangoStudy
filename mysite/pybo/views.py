from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse
# 조회한 Question모델 데이터를 템플릿 파일을 사용하여 화면에 출력할수 있는 render함수를 사용
from django.shortcuts import render, get_object_or_404, redirect
from .models import Question
from django.utils import timezone
from .forms import QuestionForm

# def index(request):
#     return HttpResponse('pybo에 온걸 환영합니다 주현님.')

def index(request):
    """
    pybo 목록 출력
    """
    question_list = Question.objects.order_by('-create_date') # 작성한 날짜 역순으로 조회 할려고, - 가 역순
    # render함수가 템플릿을 HTML로 변환되는 과정에서 사용되는 데이터이다.
    context = {'question_list': question_list}
    # return HttpResponse("안녕하세요 pybo에 온걸 환영한다.")
    # render함수는 context에 있는 Question 모델 데이터 question_list를 pybo/question_list.html파일에 적용하여
    # HTML 코드로 변환한다. 이런 파일 (pybo/question_list.html)을 템플릿이라 부른다.
    # 템플릿은 장고의 태그를 추가로 사용할수 있는 HTML파일이라 생각하면 된다.
    return render(request, 'pybo/question_list.html', context)

def detail(request, question_id):
    """
    pybo 내용 출력
    """
    # question_id는 URL 매핑에 있던 question_id이다.
    # /pybo/2/ 페이지가 호출되면 최종으로 detail 함수의 매개변수 question_id에 2가 전달된다.
    print('쉬발', request, question_id)
    question = get_object_or_404(Question, pk=question_id)
    # question = Question.objects.get(id=question_id)
    context = {'question': question}
    print("context", context)
    return render(request, 'pybo/question_detail.html', context)

def answer_create(request, question_id):
    """
    pybo 답변 등록
    """
    print("확인요", request, question_id)
    question = get_object_or_404(Question, pk=question_id)
    question.answer_set.create(content=request.POST.get('content'), create_date=timezone.now())
    return redirect('pybo:detail', question_id=question.id)
    # content는 textarea의 값이지
    # request.POST.get('content')는 POST형식으로 전송된 form데이터 항목중 name이 content인 값을 의미
    # Answer모델이 Question 모델을 Foreign Key로 참조하고 있으므로 question.answer_set 같은 표현을 사용할수 있다.

def question_create(request):
    """
    PYbo 질문 등록
    """
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid(): # POST요청으로 받은 Form이 유효한지 확인, 유효 안하면 화면에 오류 전달
            # Form으로 Question모델 데이터를 저장하기 위한 코드 commit false는 임시저장
            question = form.save(commit=False)
            question.create_date = timezone.now()
            question.save()
            return redirect('pybo:index')
    else:
        # request.method가 GET인 경우 호출, 입력값 없이 객체 생성
        form = QuestionForm()
    context = {'form': form}
    return render(request, 'pybo/question_form.html', context)
    # form = QuestionForm() # 장고의 폼이다.
