from fastapi import FastAPI
from pydantic import BaseModel
from tools.get_transcript import get_transcript
from tools.generate_summary import generate_summary

app = FastAPI()

class SummaryRequest(BaseModel):
    room_id: str

@app.post("/summarize")
def summarize(req: SummaryRequest):
    transcript = get_transcript(req.room_id)
    summary = generate_summary(transcript)
    return {
        "room_id": req.room_id,
        "summary": summary
    }
