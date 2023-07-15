from django import forms
from pybo.models import Question, Answer

# forms.Form을 상속받으면 폼
# forms.ModelForm을 상속받으면 모델 폼이라 부른다.
# 모델 폼 객체를 저장하면 연결된 모델의 데이터를 저장할수 있다.
class QuestionForm(forms.ModelForm):
    # QuestionForm클래스는 Question모델과 연결되어 있으며
    # 필드로 subject, content를 사용한다고 정의했다.
    class Meta:
        model = Question
        fields = ['subject', 'content']
        # 한글로 보기위해 아래와 같이 라벨을 설정
        labels = {
            'subject': '제목',
            'content': '내용',
        }
        # widgets = {
        #     'subject': forms.TextInput(attrs={'class': 'form-control'}),
        #     'content': forms.Textarea(attrs={'class':'form-control', 'rows': 10})
        # }
        
class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['content']
        labels = {
            'content': '답변내용',
        }