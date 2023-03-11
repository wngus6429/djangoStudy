from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from ..models import Question
from django.utils import timezone
from ..forms import QuestionForm
from django.core.paginator import Paginator # 게시물 페이지 만들기


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
