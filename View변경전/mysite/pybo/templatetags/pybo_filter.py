from django import template

register = template.Library()

@register.filter # 애너테이션, 템플릿에서 해당 함수를 필터로 사용
def sub(value, arg):
    return value - arg