CREATE TABLE IF NOT EXISTS transcripts (
    id SERIAL PRIMARY KEY,
    room_id TEXT NOT NULL,
    speaker_id TEXT NOT NULL,
    text TEXT NOT NULL,
    timestamp TIMESTAMP NOT NULL
);

INSERT INTO transcripts (room_id, speaker_id, text, timestamp) VALUES
('test-room', 'user-1', '프로젝트 일정 조정이 필요합니다.', '2025-07-01 10:00:00'),
('team-sync', 'user-4', '팀 전체 회의는 내일 오전 9시입니다.', '2025-07-01 10:00:05'),
('test-room', 'user-2', '디자인 시안은 오늘 중으로 공유하겠습니다.', '2025-07-01 10:00:10'),
('team-sync', 'user-5', 'SNS 캠페인은 다음 주부터 시작합니다.', '2025-07-01 10:00:15'),
('test-room', 'user-3', 'QA는 다음 주까지 완료 예정입니다.', '2025-07-01 10:00:20');