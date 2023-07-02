from django.contrib import admin
from .models import Question
# Register your models here.

class QuestionAdmin(admin.ModelAdmin):
    # 장고 Admin에서 제목으로 검색 가능하게끔
    search_fields = ['subject']

# 이렇게 등록해두면 장고 Admin에서 손쉽게 관리 할수 있음.
# 셸로 수행했던 데이터 저장, 수정, 삭제등의 작업을 장고에서 가능
admin.site.register(Question, QuestionAdmin)
