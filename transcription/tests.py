import io
import os
from django.test import TestCase, override_settings
from rest_framework.parsers import MultiPartParser, JSONParser
from rest_framework.test import APIClient
from .models import File, Transcription


class AudioTranscriptionAPITest(TestCase):
    def __init__(self, methodName: str = ...):
        super().__init__(methodName)

    def setUp(self):
        self.client = APIClient()
        self.valid_audio_path = os.path.join(os.path.dirname(__file__), 'test_files', '18s audio.wav')
        self.invalid_audio_path = os.path.join(os.path.dirname(__file__), 'test_files', '18s audio.wav')
        self.missing_file_response = {'message': 'Audio file or URL not provided'}
        self.invalid_token_response = {'message': 'Transcription request failed'}
        self.failed_transcription_response = {'message': 'Transcription failed'}
        self.missing_token_response = {'message': 'Deepgram API token is missing'}
        self.client.credentials()
        os.environ['DEEPGRAM_API_TOKEN'] = '6d054a01594671758512f2959832c4863ff8d2b5'

    def test_successful_transcription(self):
        with open(self.valid_audio_path, 'rb') as audio_file:
            response = self.client.post('/api/v1/transcribe/audio-to-text', {'audio_file': audio_file},
                                        format='multipart')
            self.assertEqual(response.status_code, 200)
            self.assertTrue('transcription_text' in response.data)

    def test_missing_file(self):
        response = self.client.post('/api/v1/transcribe/audio-to-text', {}, format='multipart')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, self.missing_file_response)

    def test_invalid_token(self):
        os.environ['DEEPGRAM_API_TOKEN'] = 'invalid_token'
        with open(self.valid_audio_path, 'rb') as audio_file:
            response = self.client.post('/api/v1/transcribe/audio-to-text', {'audio_file': audio_file},
                                        format='multipart')
            self.assertEqual(response.status_code, 400)
            self.assertEqual(response.data, self.invalid_token_response)

    def test_missing_token(self):
        os.environ['DEEPGRAM_API_TOKEN'] = ''
        with open(self.valid_audio_path, 'rb') as audio_file:
            response = self.client.post('/api/v1/transcribe/audio-to-text', {'audio_file': audio_file},
                                        format='multipart')
            self.assertEqual(response.status_code, 400)
            self.assertEqual(response.data, self.missing_token_response)
