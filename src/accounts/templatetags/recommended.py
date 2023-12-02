from django import template
from django.contrib.auth import get_user_model

from accounts.models import UserProfile


register = template.Library()
User = get_user_model()

@register.inclusion_tag('accounts/snippets/recommended.html')
def recommended(user):
  if isinstance(user, User):
    qs = UserProfile.objects.recommended(user)
    return {'recommended': qs}



# from django.contrib.auth import get_user_model
# from django import template
# from django.template.loader import get_template
# from django.utils.safestring import mark_safe

# from accounts.models import UserProfile

# register = template.Library()
# User = get_user_model()

# @register.simple_tag # @register.simple_tag(is_safe=True)
# def recommended(user):
#   if isinstance(user, User):
#     template = get_template('accounts/snippets/recommended.html')
#     context = {'recommended': UserProfile.objects.recommended(user)}
#     data = template.render(context=context, request=None)
#     content = mark_safe(data) # @register.filter(is_safe=True)
#     return content
#   return ''