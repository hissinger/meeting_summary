CREATE TABLE IF NOT EXISTS transcripts (
    id SERIAL PRIMARY KEY,
    room_id TEXT NOT NULL,
    speaker_id TEXT NOT NULL,
    text TEXT NOT NULL,
    timestamp TIMESTAMP NOT NULL
);

INSERT INTO transcripts (room_id, speaker_id, text, timestamp) VALUES
('test-room', 'alice', '프로젝트 일정 조정이 필요합니다.', '2025-07-01 10:00:00'),
('team-sync', 'david', '팀 전체 회의는 내일 오전 9시입니다.', '2025-07-01 10:00:05'),
('test-room', 'bob', '디자인 시안은 오늘 중으로 공유하겠습니다.', '2025-07-01 10:00:10'),
('team-sync', 'emma', 'SNS 캠페인은 다음 주부터 시작합니다.', '2025-07-01 10:00:15'),
('test-room', 'carol', 'QA는 다음 주까지 완료 예정입니다.', '2025-07-01 10:00:20');