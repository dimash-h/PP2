-- Основная таблица контактов 
CREATE TABLE IF NOT EXISTS contacts (
    id    SERIAL PRIMARY KEY,
    name  VARCHAR(255) NOT NULL,
    phone VARCHAR(20)  NOT NULL
);

-- Таблица групп
CREATE TABLE IF NOT EXISTS groups (
    id   SERIAL PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL
);

-- Стандартные группы
INSERT INTO groups (name) VALUES ('Family'), ('Work'), ('Friend'), ('Other')
ON CONFLICT (name) DO NOTHING;

-- Новые поля в contacts (БЕЗ удаления phone!)
ALTER TABLE contacts ADD COLUMN IF NOT EXISTS email    VARCHAR(100);
ALTER TABLE contacts ADD COLUMN IF NOT EXISTS birthday DATE;
ALTER TABLE contacts ADD COLUMN IF NOT EXISTS group_id INTEGER REFERENCES groups(id);

-- Таблица для дополнительных телефонов
CREATE TABLE IF NOT EXISTS phones (
    id         SERIAL PRIMARY KEY,
    contact_id INTEGER REFERENCES contacts(id) ON DELETE CASCADE,
    phone      VARCHAR(20)  NOT NULL,
    type       VARCHAR(10)  CHECK (type IN ('home', 'work', 'mobile'))
);
