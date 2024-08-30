from django.http import HttpResponse
from django.template.loader import render_to_string

def index(request):
    print(request)
    return HttpResponse(render_to_string(template_name='base.html', context={}, request=request))