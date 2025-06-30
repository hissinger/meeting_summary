from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_summary(transcript: list[dict]) -> dict:
    text = "\n".join(f"{t['speaker_id']}: {t['text']}" for t in transcript)
    prompt = (
        "다음 회의 내용을 바탕으로:\n"
        "1. 주요 논의 내용을 자세히 요약하고,\n"
        "2. 회의에서 결정된 액션 아이템들을 항목으로 정리해줘.\n\n"
        f"{text}"
    )

    response = client.chat.completions.create(
        model="gpt-4-turbo",
        messages=[
            {"role": "system", "content": "너는 회의 요약 도우미야."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3,
    )

    content = response.choices[0].message.content.strip()
    return {"summary": content}