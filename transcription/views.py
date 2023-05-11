import os

from django.http import FileResponse
from drf_yasg.openapi import Schema, TYPE_FILE
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import APIView, parser_classes
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework import status

from transcription.lib.audio_transcription import AudioTranscription


class AudioTranscriptionAPI(APIView):
    """
    API endpoint that accepts an audio file and transcribes it into text using the Deepgram API.
    """

    @swagger_auto_schema(
        request_body=Schema(
            type=TYPE_FILE,
            description="Audio file in .wav or .mp3 format"
        ),
        responses={
            200: Schema(
                type="object",
                properties={
                    "transcription_text": Schema(
                        type="string",
                        description="Transcription result in text format"
                    )
                }
            ),
            400: "Bad Request"
        }
    )
    @parser_classes([MultiPartParser])
    def post(self, request, format=None):
        """
        Transcribes the provided audio file and returns the transcription result in text format.
        """
        audio_file = request.FILES.get('audio_file')
        api_token = os.getenv('DEEPGRAM_API_TOKEN')

        if not audio_file:
            return Response({'message': 'Audio file not provided'}, status=status.HTTP_400_BAD_REQUEST)

        audio_transcription = AudioTranscription(api_token)

        try:
            transcription_text = audio_transcription.transcribe(audio_file.read())
        except ValueError as e:
            return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'transcription_text': transcription_text}, status=status.HTTP_200_OK)
