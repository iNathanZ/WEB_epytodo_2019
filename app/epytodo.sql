CREATE DATABASE IF NOT EXISTS epytodo;
USE epytodo;
CREATE TABLE IF NOT EXISTS user (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS task (
    task_id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    begin TIMESTAMP  DEFAULT CURRENT_TIMESTAMP,
    end DATE DEFAULT NULL,
    status ENUM('not started', 'in progress', 'done') DEFAULT 'not started'
);

CREATE TABLE  IF NOT EXISTS user_has_task (
    fk_user_id INT,
    fk_task_id INT,
    PRIMARY KEY (fk_user_id, fk_task_id),
    FOREIGN KEY (fk_user_id)
        REFERENCES user (user_id)
        ON DELETE CASCADE,
    FOREIGN KEY (fk_task_id)
        REFERENCES task (task_id)
        ON DELETE CASCADE
);