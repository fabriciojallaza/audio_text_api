from django.urls import path

from transcription.views import AudioTranscriptionAPI

app_name = 'transcription'

urlpatterns = [
    path('audio-to-text', AudioTranscriptionAPI.as_view(), name='audio-to-text'),
]
