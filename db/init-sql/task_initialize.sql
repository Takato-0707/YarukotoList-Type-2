-- テーブル作成
-- ジャンル管理用テーブル
CREATE TABLE IF NOT EXISTS genre (
    genre_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE
);

-- タスク管理用テーブル
CREATE TABLE IF NOT EXISTS task (
    task_id SERIAL PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    genre_id INTEGER REFERENCES genre(genre_id) ON UPDATE CASCADE ON DELETE
    SET NULL
);

-- タスクの曜日指定用テーブル
CREATE TABLE IF NOT EXISTS task_weekday (
    task_weekday_id SERIAL PRIMARY KEY,
    task_id INTEGER NOT NULL REFERENCES task(task_id) ON UPDATE CASCADE ON DELETE CASCADE,
    weekday SMALLINT NOT NULL CHECK (
        weekday BETWEEN 0
        AND 6
    ),
    UNIQUE (task_id, weekday)
);

-- タスクの実行記録管理用テーブル
CREATE TABLE IF NOT EXISTS task_log (
    task_id INTEGER NOT NULL REFERENCES task(task_id) ON UPDATE CASCADE ON DELETE CASCADE,
    date DATE NOT NULL,
    is_completed BOOLEAN NOT NULL DEFAULT FALSE,
    completed_at TIMESTAMP,
    UNIQUE (task_id, date)
);

-- 初期データ挿入
INSERT INTO genre (name) VALUES
    ('健康'),
    ('学習'),
    ('仕事'),
    ('家事'),
    ('趣味');

INSERT INTO task (title, description, genre_id) VALUES
    ('毎朝の散歩', '毎朝20分間散歩をする', 1);

INSERT INTO task_weekday (task_id, weekday) VALUES
-- 毎朝の散歩
    (1, 0),
    (1, 1),
    (1, 2),
    (1, 3),
    (1, 4),
    (1, 5),
    (1, 6);

INSERT INTO task_log (task_id, date, is_completed, completed_at) VALUES
    (1, '2025-01-01', TRUE, '2025-01-01 07:30:00');