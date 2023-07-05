
import numpy as np

from django.conf import settings
from shared.services.data_service import DataService

def create_survey_for_user(user_code):
    data_service = DataService()
    conversations = get_random_conversations(data_service)
    data_service.create_user_survey(conversations, user_code)


def get_random_conversations(service):
    conversations = service.get_conversations()
    num_of_conversations_per_survey = settings.NUM_OF_CONVERSATIONS_PER_SURVEY
    np.random.shuffle(conversations)
    return conversations[:num_of_conversations_per_survey]