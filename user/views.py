
from django.http import JsonResponse, HttpResponseNotAllowed, Http404

from survey.services.survey_service import create_survey_for_user
from .permissions import is_allowed_to_register
from .services.user_service import get_registration_data, get_registration_code, add_user


@is_allowed_to_register
def register(request):
    if request.method != 'POST':
        return HttpResponseNotAllowed()
    
    success, registration_data = get_registration_data(request)
    if not success:
        return Http404()
    
    code = get_registration_code(registration_data)
    registration_data.append(code) 
    add_user(registration_data)

    create_survey_for_user(code)

    return JsonResponse({'message': 'OK', 'content': {'registration_code': code}})
