from django import template
from django.http import QueryDict
from django.template.context import RequestContext

register = template.Library()


@register.simple_tag(takes_context=True)
def saving_parameters_request(context: RequestContext, page_number: int) -> str:
    request = context.get('request')
    parameters_get: QueryDict = request.GET.copy()
    parameters_get['page'] = page_number
    return parameters_get.urlencode()
