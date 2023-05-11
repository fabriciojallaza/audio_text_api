import mimetypes

import requests
import json

from transcription.models import File, Transcription


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
        data, mime_type = self._set_data(audio_file)
        headers = self._set_headers(mime_type)

        response = self._send_request(headers, data)
        transcription_text = self._handle_response(response)

        #store transcription_text in database
        file_storage = self._file_storage(audio_file)
        transcription_storage = self._transcription_storage(transcription_text, file_storage)

        #verify if transcription_text is an object
        if isinstance(transcription_text, object):
            pass
        else:
            raise ValueError('Transcription request failed, transcription was not stored in database')

        return transcription_text

    def _set_headers(self, mime_type):
        if not self.api_token:
            raise ValueError('Deepgram API token is missing')
        return {'Authorization': f'Token {self.api_token}',
                'Content-Type': mime_type}

    def _set_data(self, audio_file):
        # differentiate from file upload or url
        if isinstance(audio_file, str):
            # call set_headers
            mime_type = 'application/json'
            return json.dumps({"url": audio_file}), mime_type
        else:
            # change content-type header and detect MIME type
            mime_type = mimetypes.guess_type(audio_file.name)[0]
            return audio_file.read(), mime_type

    def _send_request(self, headers, data):
        try:
            response = requests.post(self.url, headers=headers, data=data)
        except requests.exceptions.RequestException:
            raise ValueError('Transcription request failed')
        return response

    def _handle_response(self, response):
        if response.status_code == 200:
            response_data = json.loads(response.content)
            transcription_text = response_data['results']['channels'][0]['alternatives'][0]['transcript']
            return transcription_text
        elif response.status_code == 401:
            raise ValueError('Invalid Deepgram API token')
        else:
            raise ValueError('Transcription failed')

    def _file_storage(self, audio_file):
        file = File()
        file.file = audio_file
        file.name = audio_file if isinstance(audio_file, str) else audio_file.name
        file.save()
        return file

    def _transcription_storage(self, transcription_text, file_storage):
        transcription = Transcription()
        transcription.text = transcription_text
        transcription.file = file_storage
        transcription.save()
        return transcription
