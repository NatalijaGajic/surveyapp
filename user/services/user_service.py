import json
from datetime import datetime

from django.core.signing import Signer
from shared.services.data_service import DataService

# TODO user cant be registered twice
def get_registration_code(registration_data):
    first_name, last_name, _ = registration_data
    value_to_sign = f'{first_name}_{last_name}'
    signer = Signer()
    signed_value = signer.sign(value_to_sign).split(':')[1]
    return signed_value


def get_registration_data(request):
    try:
        payload = json.loads(request.body)
        first_name, last_name = payload['first_name'], payload['last_name']
        registration_time = datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
        return True, [first_name, last_name, registration_time]
    except:
        return False, []

def add_user(user_data):
    service = DataService()
    service.add_user(user_data)