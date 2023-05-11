from django.urls import path

from transcription import views

app_name = 'transcription'

urlpatterns = [
    path('audio-to-text/', views.audio_to_text, name='audio_to_text'),
]
