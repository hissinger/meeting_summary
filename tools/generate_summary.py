from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.3)

prompt = ChatPromptTemplate.from_messages([
    ("system", "너는 회의 요약 도우미야."),
    ("user", """다음 회의 내용을 바탕으로:
1. 주요 논의 내용을 자세히 요약하고,
2. 회의에서 결정된 액션 아이템들을 항목으로 정리해줘.

{transcript_text}""")
])

chain = prompt | llm

def generate_summary(transcript: list[dict]) -> dict:
    transcript_text = "\n".join(f"{t['speaker_id']}: {t['text']}" for t in transcript)
    result = chain.invoke({"transcript_text": transcript_text})
    return {"summary": result.content.strip()}
