from fastapi import FastAPI
from pydantic import BaseModel
from tools.get_transcript import get_transcript
from tools.generate_summary import generate_summary
from db import get_db_connection
from datetime import datetime

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

def init_schema():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS transcripts (
                id SERIAL PRIMARY KEY,
                room_id TEXT NOT NULL,
                speaker_id TEXT NOT NULL,
                text TEXT NOT NULL,
                timestamp TIMESTAMP NOT NULL
            )
        """)
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        print("Failed to initialize schema:", e)

def init_test_data():
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("DELETE FROM transcripts WHERE room_id = %s", ('test-room',))

        cur.execute("""
            INSERT INTO transcripts (room_id, speaker_id, text, timestamp)
            VALUES 
                (%s, %s, %s, %s),
                (%s, %s, %s, %s),
                (%s, %s, %s, %s)
        """, (
            'test-room', 'user-1', '프로젝트 일정 조정이 필요합니다.', datetime(2025, 7, 1, 10, 0, 0),
            'test-room', 'user-2', '디자인 시안은 오늘 중으로 공유하겠습니다.', datetime(2025, 7, 1, 10, 0, 10),
            'test-room', 'user-3', 'QA는 다음 주까지 완료 예정입니다.', datetime(2025, 7, 1, 10, 0, 20)
        ))

        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        print("Failed to initialize test data:", e)

@app.on_event("startup")
def startup_event():
    init_schema()
    init_test_data()