from django.conf import settings

def authenticate(username, password):
    return username == settings.BASIC_AUTH_USERNAME and password == settings.BASIC_AUTH_PASSWORD