from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from transcription.views import AudioTranscriptionAPI

schema_view = get_schema_view(
    openapi.Info(
        title="Audio Transcription API",
        default_version='v1',
        description="API endpoint that accepts an audio file and transcribes it into text using the Deepgram API",
    ),
    public=True,
)

router = routers.DefaultRouter()

urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/v1/transcribe/', AudioTranscriptionAPI.as_view(), name='transcription'),
    path('api/v1/docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('api/v1/docs.json', schema_view.without_ui(cache_timeout=0), name='schema-json'),
]
