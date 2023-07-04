from django.db import models

class Session(models.Model):
    timestamp = models.DateTimeField(auto_now=True)
    # user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    
