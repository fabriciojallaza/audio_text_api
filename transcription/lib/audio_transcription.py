import requests
import json
import os


class AudioTranscription:
    """
    This class provides a method to transcribe an audio file using the Deepgram API.
    """

    def __init__(self, api_token):
        self.url = 'https://api.deepgram.com/v1/listen'
        self.api_token = api_token  # 6d054a01594671758512f2959832c4863ff8d2b5

    def transcribe(self, audio_file):
        """
        Transcribes an audio file using the Deepgram API.
        """
        headers = self._set_headers()
        data = self._set_data(audio_file)

        response = self._send_request(headers, data)
        transcription_text = self._handle_response(response)

        return transcription_text

    def _set_headers(self):
        if not self.api_token:
            raise ValueError('Deepgram API token is missing')
        return {'Authorization': f'Token {self.api_token}',
                'content-type': 'application/json'}

    def _set_data(self, audio_file):
        return {'audio': audio_file}

    def _send_request(self, headers, data):
        try:
            response = requests.post(self.url, headers=headers, data=data)
        except requests.exceptions.RequestException:
            raise ValueError('Transcription request failed')
        return response

    def _handle_response(self, response):
        if response.status_code == 200:
            response_data = json.loads(response.content)
            transcription_text = response_data['results']['channel_0'][0]['text']
            return transcription_text
        elif response.status_code == 401:
            raise ValueError('Invalid Deepgram API token')
        else:
            raise ValueError('Transcription failed')
