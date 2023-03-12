from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Question(models.Model):
    # 계정이 삭제되면 계정과 연결된 Question 모델 데이터를 삭제. Question과 연결된 답변도 사라지겠지.
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author_question')
    # 글자수 제한을 위해서는 CharField를 사용
    subject = models.CharField(max_length=200)
    content = models.TextField()  # textfield는 제한 없음.
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField(null=True, blank=True)
    voter = models.ManyToManyField(User, related_name='voter_question')
    # blank=True는 form.is_valid()를 통한 입력 폼 데이터 검사시 값이 없어도 된다는것.
    # 즉 null=True, blank=True 로 인해 어떤 조건으로든 값을 비워둘수 있다는것
    def __str__(self):
        # 이렇게 해야 자세한 내용이 보인다
        return self.subject

class Answer(models.Model):
    # 어떤 모델이 다른 모델을 속성으로 가지면 ForeignKey를 이용.(다른 모델과의 연결)
    # on_delete=model.CASCADE는 답변에 연결된 질문이 삭제되면 답변도 함께 삭제해라.
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author_answer')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    content = models.TextField()
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField(null=True, blank=True)
    voter = models.ManyToManyField(User, related_name='voter_answer')
    def __str__(self):
        # 이렇게 해야 자세한 내용이 보인다
        return self.question

class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField(null=True, blank=True)
    question = models.ForeignKey(Question, null=True, blank=True, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, null=True, blank=True, on_delete=models.CASCADE)
