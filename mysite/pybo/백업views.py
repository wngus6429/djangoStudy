# 조회한 Question모델 데이터를 템플릿 파일을 사용하여 화면에 출력할수 있는 render함수를 사용
# from django.shortcuts import render, get_object_or_404, redirect
# from django.contrib.auth.decorators import login_required
# from django.contrib import messages
# from .models import Question, Answer, Comment
# from django.utils import timezone
# from .forms import QuestionForm, AnswerForm, CommentForm
# from django.core.paginator import Paginator # 게시물 페이지 만들기

# from django.http import HttpResponse
# def index(request):
#     return HttpResponse('pybo에 온걸 환영합니다 주현님.')

#
# # login_required 애너테이션을 통해 로그인 검사
# @login_required(login_url='common:login')
# def answer_create(request, question_id):
#     """
#     pybo 답변 등록
#     """
#     print("확인요", request, question_id)
#     question = get_object_or_404(Question, pk=question_id)
#     if request.method == "POST":
#         form = AnswerForm(request.POST)
#         if form.is_valid():
#             answer = form.save(commit=False)
#             answer.author = request.user # 추가한 속성 author 적용
#             answer.create_date = timezone.now()
#             answer.question = question
#             answer.save()
#             return redirect('pybo:detail', question_id=question.id)
#     else:
#         form = AnswerForm()
#     context = {'question': question, 'form': form}
#     return render(request, 'pybo/question_detail.html', context)
#     # question.answer_set.create(content=request.POST.get('content'), create_date=timezone.now())
#     # return redirect('pybo:detail', question_id=question.id)
#     # content는 textarea의 값이지
#     # request.POST.get('content')는 POST형식으로 전송된 form데이터 항목중 name이 content인 값을 의미
#     # Answer모델이 Question 모델을 Foreign Key로 참조하고 있으므로 question.answer_set 같은 표현을 사용할수 있다.
#
# @login_required(login_url='common:login')
# def answer_modify(request, answer_id):
#     """
#     pybo 답변 수정
#     """
#     # get_object_or_404 함수는 Django에서 제공하는 단축 함수로, 첫 번째 인자로 모델 클래스(Model Class)를,
#     # 두 번째 인자로는 검색 조건을 전달받아 해당 조건으로 검색된 객체(Object)를 반환합니다.
#     # 검색된 객체가 존재하지 않는 경우, Http404 예외를 발생시킵니다.
#     # 여기서 pk=answer_id는 Answer 모델에서 pk 필드 값이 answer_id인 레코드를 검색하겠다는 의미입니다. 즉, answer_id는 Answer 모델에서 특정 레코드를 식별하는 기본 키 값입니다
#     answer = get_object_or_404(Answer, pk=answer_id)
#     if request.user != answer.author:
#         messages.error(request, '수정권한이 없습니다.')
#         return redirect('pybo:detail', question_id=answer.question.id)
#
#     if request.method == "POST":
#         form = AnswerForm(request.POST, instance=answer)
#         if form.is_valid():
#             answer = form.save(commit=False)
#             answer.author = request.user
#             answer.modify_date = timezone.now()
#             answer.save()
#             return redirect('pybo:detail', question_id=answer.question_id)
#     else:
#         form = AnswerForm(instance=answer)
#     context = {'answer':answer, 'form':form}
#     return render(request, 'pybo/answer_form.html', context)
#
# @login_required(login_url='common:login')
# def answer_delete(request, answer_id):
#     """
#     답변 삭제
#     """
#     answer = get_object_or_404(Answer, pk=answer_id)
#     if request.user != answer.author:
#         messages.error('request', '삭제 권한이 없습니다')
#     else:
#         answer.delete()
#     return redirect('pybo:detail', question_id=answer.question.id)
