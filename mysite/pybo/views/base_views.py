from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from ..models import Question

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
