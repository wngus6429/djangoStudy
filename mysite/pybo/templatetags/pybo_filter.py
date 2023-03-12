import markdown
from django import template
from django.utils.safestring import mark_safe

register = template.Library()

# 애너테이션, 템플릿에서 해당 함수를 필터로 사용
@register.filter
def sub(value, arg):
    return value - arg

@register.filter()
def mark(value):
    extensions = ["nl2br", "fenced_code"]
    return mark_safe(markdown.markdown(value, extensions=extensions))
    # nl2br는 줄바꿈 문자를 <br>태그로 바꿔줌, enter한번만 눌러도 줄바꿈 인식.
    # fenced_code 는 마크다운의 소스 코드 표현을 위해 적용했다.