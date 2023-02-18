from django.db import models

# Create your models here.

class Question(models.Model):
    # 글자수 제한을 위해서는 CharField를 사용
    subject = models.CharField(max_length=200)
    content = models.TextField() #textfield는 제한 없음.
    create_date = models.DateTimeField()

class Answer(models.Model):
    # 어떤 모델이 다른 모델을 속성으로 가지면 ForeignKey를 이용.(다른 모델과의 연결)
    # on_delete=model.CASCADE는 답변에 연결된 질문이 삭제되면 답변도 함께 삭제해라.
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    content = models.TextField()
    create_date = models.DateTimeField()