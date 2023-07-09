from django.urls import path

from . import views

urlpatterns = [
    path('', views.index),
    path('start-survey/', views.start_survey),
    path('rate-conversation/', views.rate_conversation),
    path('give-reason/', views.give_reason),
    path('end-survey/', views.end_survey)
]
