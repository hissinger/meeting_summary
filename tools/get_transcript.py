from db import get_db_connection

def get_transcript(room_id: str) -> list[dict]:
    """
    특정 room_id에 해당하는 회의 내용을 시간순으로 반환합니다.
    각 항목은 {speaker_id, text, timestamp} 형태입니다.
    """
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT speaker_id, text, timestamp
        FROM transcripts
        WHERE room_id = %s
        ORDER BY timestamp ASC
    """, (room_id,))
    rows = cur.fetchall()
    cur.close()
    conn.close()

    return [
        {
            "speaker_id": row[0],
            "text": row[1],
            "timestamp": row[2].isoformat()
        }
        for row in rows
    ]