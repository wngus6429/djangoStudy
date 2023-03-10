# 조회한 Question모델 데이터를 템플릿 파일을 사용하여 화면에 출력할수 있는 render함수를 사용
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Question, Answer
from django.utils import timezone
from .forms import QuestionForm, AnswerForm
from django.core.paginator import Paginator # 게시물 페이지 만들기

# from django.http import HttpResponse
# def index(request):
#     return HttpResponse('pybo에 온걸 환영합니다 주현님.')

def index(request):
    """
    pybo 목록 출력
    """
    # 입력 인자, localhost:8000/pybo/?page=1 이런식
    page = request.GET.get('page', '1') # 페이지
    # get('page', '1')에서 '1'은 /pybo/ 처럼 ?page=1과 같은 page 파라미터가 없는 URL을 위해
    # 기본값으로 1을 지정한 것이다. 페이지 구현에 사용한 클래스는 Paginator이다.

    # 조회
    question_list = Question.objects.order_by('-create_date')

    # 페이징 처리
    paginator = Paginator(question_list, 5) # 페이지당 10개씩 보여주기
    page_obj = paginator.get_page(page)
    # question_list = Question.objects.order_by('-create_date') # 작성한 날짜 역순으로 조회 할려고, - 가 역순
    # context = {'question_list': question_list}

    context = {'question_list': page_obj}
    return render(request, 'pybo/question_list.html', context)
    # render 함수가 템플릿을 HTML로 변환되는 과정에서 사용되는 데이터이다.
    # return HttpResponse("안녕하세요 pybo에 온걸 환영한다.")
    # render 함수는 context에 있는 Question 모델 데이터 question_list를 pybo/question_list.html파일에 적용하여
    # HTML 코드로 변환한다. 이런 파일 (pybo/question_list.html)을 템플릿이라 부른다.
    # 템플릿은 장고의 태그를 추가로 사용할수 있는 HTML파일이라 생각하면 된다.

def detail(request, question_id):
    """
    pybo 내용 출력
    """
    # question_id는 URL 매핑에 있던 question_id이다.
    # /pybo/2/ 페이지가 호출되면 최종으로 detail 함수의 매개변수 question_id에 2가 전달된다.
    question = get_object_or_404(Question, pk=question_id)
    # question = Question.objects.get(id=question_id)
    context = {'question': question}
    print('Detail페이지', context)
    return render(request, 'pybo/question_detail.html', context)

# login_required 애너테이션을 통해 로그인 검사
@login_required(login_url='common:login')
def answer_create(request, question_id):
    """
    pybo 답변 등록
    """
    print("확인요", request, question_id)
    question = get_object_or_404(Question, pk=question_id)
    if request.method == "POST":
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.author = request.user # 추가한 속성 author 적용
            answer.create_date = timezone.now()
            answer.question = question
            answer.save()
            return redirect('pybo:detail', question_id=question.id)
    else:
        form = AnswerForm()
    context = {'question': question, 'form': form}
    return render(request, 'pybo/question_detail.html', context)
    # question.answer_set.create(content=request.POST.get('content'), create_date=timezone.now())
    # return redirect('pybo:detail', question_id=question.id)
    # content는 textarea의 값이지
    # request.POST.get('content')는 POST형식으로 전송된 form데이터 항목중 name이 content인 값을 의미
    # Answer모델이 Question 모델을 Foreign Key로 참조하고 있으므로 question.answer_set 같은 표현을 사용할수 있다.

@login_required(login_url='common:login')
def question_create(request):
    """
    PYbo 질문 등록
    """
    print('질문만들기request', request.user)
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        # POST요청으로 받은 Form이 유효한지 확인, 유효 안하면 화면에 오류 전달
        print("form", form)
        if form.is_valid():
            # Form으로 Question모델 데이터를 저장하기 위한 코드 commit false는 임시저장
            question = form.save(commit=False)
            question.author = request.user  # 추가한 속성 author 적용
            question.create_date = timezone.now()
            question.save()
            return redirect('pybo:index')
    else:
        # get인 경우는 질문 작성할려고 폼이 텅빈 상태
        # request.method가 GET인 경우 호출, 입력값 없이 객체 생성
        form = QuestionForm()
    context = {'form': form}
    return render(request, 'pybo/question_form.html', context)
    # form = QuestionForm() # 장고의 폼이다.

@login_required(login_url='common:login')
def question_modify(request, question_id):
    """
    pybo질문수정
    """
    # request.user = 로그인한 사용자, question.author = 글쓴이
    question = get_object_or_404(Question, pk=question_id)
    if request.user != question.author:
        messages.error(request, "수정권한이 없습니다.")
        return redirect('pybo:detail', question_id=question.id)
    if request.method == "POST":
        # 질문 수정화면에서 <저장하기>를 누르면 /pybo/question/modify/2/ 페이지 Post방식 호출
        form = QuestionForm(request.POST, instance=question)
        if form.is_valid():
            question = form.save(commit=False)
            question.author = request.user
            question.modify_date = timezone.now() # 수정일시 저장
            question.save()
            return redirect('pybo:detail', question_id=question.id)
    else:
        # /pybo/question/modify/2/ 페이지 GET요청
        # 기존에 저장되어 있던 제목, 내용이 반영된 상태에서 수정 가능하게 폼 생성
        form = QuestionForm(instance=question)
    context = {'form': form}
    return render(request, 'pybo/question_form.html', context)
# 데이터 저장시 form 엘리먼트에 action 속성이 없으면 현재의 페이지로 폼을 전송한다.
# 질문 수정에서 사용한 템플릿은 질문 등록시 사용한 pybo/question_form.html 파일을 그대로 사용한다.
@login_required(login_url='common:login') # 로그인한 사용자와 글쓴이가 동일한가.
def question_delete(request, question_id):
    """
    질문삭제
    """
    question = get_object_or_404(Question, pk=question_id)
    if request.user != question.author:
        messages.error(request, '삭제권한이 없습니다')
        return redirect('pybo:detail', question_id=question_id)
    question.delete()
    return redirect('pybo:index')

@login_required(login_url='common:login')
def answer_modify(request, answer_id):
    """
    pybo 답변 수정
    """
    # get_object_or_404 함수는 Django에서 제공하는 단축 함수로, 첫 번째 인자로 모델 클래스(Model Class)를,
    # 두 번째 인자로는 검색 조건을 전달받아 해당 조건으로 검색된 객체(Object)를 반환합니다.
    # 검색된 객체가 존재하지 않는 경우, Http404 예외를 발생시킵니다.
    # 여기서 pk=answer_id는 Answer 모델에서 pk 필드 값이 answer_id인 레코드를 검색하겠다는 의미입니다. 즉, answer_id는 Answer 모델에서 특정 레코드를 식별하는 기본 키 값입니다
    answer = get_object_or_404(Answer, pk=answer_id)
    if request.user != answer.author:
        messages.error(request, '수정권한이 없습니다.')
        return redirect('pybo:detail', question_id=answer.question.id)

    if request.method == "POST":
        form = AnswerForm(request.POST, instance=answer)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.author = request.user
            answer.modify_date = timezone.now()
            answer.save()
            return redirect('pybo:detail', question_id=answer.question_id)
    else:
        form = AnswerForm(instance=answer)
    context = {'answer':answer, 'form':form}
    return render(request, 'pybo/answer_form.html', context)

@login_required(login_url='common:login')
def answer_delete(request, answer_id):
    """
    답변 삭제
    """
    answer = get_object_or_404(Answer, pk=answer_id)
    if request.user != answer.author:
        messages.error('request', '삭제 권한이 없습니다')
    else:
        answer.delete()
    return redirect('pybo:detail', question_id=answer.question.id)
