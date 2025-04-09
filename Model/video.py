import uuid
from urllib.parse import urlparse, parse_qs
from pydantic import BaseModel
from typing import Optional
from youtube_transcript_api import YouTubeTranscriptApi

class Video(BaseModel):
    id: str
    url: str
    videoID: str

    @classmethod
    def create(cls, url: str):
        
        yt_id = cls.take_youtube_id(url)

        return cls(id=str(uuid.uuid4()), url=url, videoID=yt_id)

    @classmethod
    def take_youtube_id(cls, url):
        query = urlparse(url)

        # Verifica a estrutura da URL
        if query.hostname == 'youtu.be':
            return query.path[1:]  # Retorna o ID após a barra

        if query.hostname in ('www.youtube.com', 'youtube.com', 'm.youtube.com'):
            if query.path == '/watch':
                # Usando split para pegar o ID do vídeo
                params = query.query.split('&')
                for param in params:
                    key_value = param.split('=')
                    if key_value[0] == 'v':
                        return key_value[1]  # Retorna o valor associado à chave 'v'

            if query.path.startswith('/embed/') or query.path.startswith('/v/'):
                return query.path.split('/')[2]  # Retorna o ID do vídeo
        return None

    @classmethod
    def get_transcription(cls, video_id):
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['en', 'pt'])
        full_transcript = " ".join([i['text'] for i in transcript])

        return full_transcript
