import pandas as pd

from django.conf import settings


class DataService():

    def get_conversations(self):
        conversations_df = pd.read_excel(settings.CONVERSATIONS_PATH)
        return conversations_df['file_name'].to_numpy()
    
    def create_user_survey(self, conversations, code):
        user_survey_df = pd.DataFrame(columns=['conversation', 'start_time', 'end_time', 'rating', 'reason'])
        user_survey_df['conversation'] = conversations
        file_path = settings.USERS_SURVEYS_DIR + r'\{}.xlsx'.format(code)
        user_survey_df.to_excel(file_path, engine='xlsxwriter')


