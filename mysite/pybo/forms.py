from django import forms
from pybo.models import Question

# forms.Form을 상속받으면 폼
# forms.ModelForm을 상속받으면 모델 폼이라 부른다.
# 모델 폼 객체를 저장하면 연결된 모델의 데이터를 저장할수 있다.
class QuestionForm(forms.ModelForm):
    # QuestionForm클래스는 Question모델과 연결되어 있으며
    # 필드로 subject, content를 사용한다고 정의했다.
    class Meta:
        model = Question
        fields = ['subject', 'content']