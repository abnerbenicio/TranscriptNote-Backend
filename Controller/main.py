from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from Model.video import Video
from Model.VideoRequest import VideoRequest
import whisper

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/v1/")
async def read():
    return {"Hello": "World"}

@app.post("/api/v1/video-transcript")
async def create_item(request: VideoRequest):
    video = Video.create(request.url)
    transcript = video.get_transcription(video.videoID)
    return {"summary":transcript}

@app.post("/api/v1/audio-transcript")
async def transcript_audio(file: UploadFile = File(...)):
    model = whisper.load_model("base")
    audio_path = "uploaded_audio.mp3"
    with open(audio_path, "wb") as f:
        f.write(await file.read())

    # Transcreva o áudio usando Whisper
    result = model.transcribe(audio_path)
    text = result['text']

    return {"Transcription": text}
    