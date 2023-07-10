import base64

from django.http import HttpResponse
from .services.auth_service import authenticate

def view_or_basicauth(view, request, *args, **kwargs):

    if 'HTTP_AUTHORIZATION' in request.META:
        auth = request.META['HTTP_AUTHORIZATION'].split()
        if len(auth) == 2:
            if auth[0].lower() == "basic":
                # TODO uname, passwd = base64.b64decode(auth[1]).split(':')
                uname, passwd = auth[1].split(':')
                success = authenticate(username=uname, password=passwd)
                if success:
                    return view(request, *args, **kwargs)
                        
    response = HttpResponse()
    response.status_code = 401
    return response


def is_allowed_to_register(func):
    def wrapper(request, *args, **kwargs):
        return view_or_basicauth(func, request, *args, **kwargs)
    return wrapper

def is_allowed_to_reset_survey(func):
    def wrapper(request, *args, **kwargs):
        return view_or_basicauth(func, request, *args, **kwargs)
    return wrapper