import json
from datetime import datetime

from django.core.signing import Signer


def get_registration_code(request):
    try:
        payload = json.loads(request.body)
        first_name, last_name = payload['first_name'], payload['last_name']
        registration_time = datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
        value_to_sign = f'{first_name}_{last_name}_{registration_time}'
        signer = Signer()
        signed_value = signer.sign(value_to_sign).split(':')[1]
        return True, signed_value
    except:
        False, ''