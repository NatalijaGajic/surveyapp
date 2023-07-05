from django.http import HttpResponse, HttpResponseNotAllowed
from .permissions import is_allowed_to_register

@is_allowed_to_register
def register(request):
    if request.method != 'POST':
        return HttpResponseNotAllowed()
    
    return HttpResponse('OK')
