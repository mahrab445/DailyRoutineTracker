CREATE DATABASE IF NOT EXISTS daily_routine;

USE daily_routine;

CREATE TABLE tasks (
    id INT AUTO_INCREMENT PRIMARY KEY,
    task_name VARCHAR(100) NOT NULL
);

INSERT INTO tasks (task_name) VALUES
('Wake Up'),
('Fajr Prayer'),
('Breakfast'),
('Study'),
('Coding Practice'),
('Lunch'),
('Exercise'),
('Dinner'),
('Sleep');

CREATE TABLE routine_status (
    id INT AUTO_INCREMENT PRIMARY KEY,
    routine_date DATE NOT NULL,
    task_id INT NOT NULL,
    status BOOLEAN DEFAULT FALSE,

    FOREIGN KEY(task_id)
    REFERENCES tasks(id)
    ON DELETE CASCADE,

    UNIQUE(routine_date, task_id)
);


USE daily_routine;

SHOW TABLES;

SELECT * FROM tasks;

DELETE FROM tasks WHERE id = 9;

COMMIT;

INSERT INTO tasks (task_name) VALUES
('Wake Up At 5.30AM'),
('Fajr Prayer'),
('Breakfast'),
('University Class'),
('Lunch'),
('Zuhr Prayer'),
('Python + Machine Learning (At least 2 hours)'),
('Asr Prayer'),
('GYM'),
('Maghrib Prayer'),
('Academic Studies (At least 3 hours)'),
('Isha Prayer'),
('Dinner'),
('Sleep (At Least 5 hours)');
