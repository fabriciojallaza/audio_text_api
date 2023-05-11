import os

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import requests
import json

from transcription.lib.audio_transcription import AudioTranscription


class AudioTranscriptionAPI(APIView):
    """
    API endpoint that accepts an audio file and transcribes it into text using the Deepgram API.
    """

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
