
DROP DATABASE chatapp;
DROP USER 'testuser';

CREATE USER 'testuser' IDENTIFIED BY 'testuser';
CREATE DATABASE chatapp;
USE chatapp;
GRANT ALL PRIVILEGES ON chatapp.* TO 'testuser';
SET NAMES utf8mb4;




CREATE TABLE users (
    user_id  VARCHAR(255) PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    nickname VARCHAR(50) NOT NULL,
    icon_image_url VARCHAR(255) DEFAULT '/static/image/icon' NULL,
    favorite VARCHAR(255) NOT NULL DEFAULT '未登録',
    bio VARCHAR(255) NULL,
    occupation VARCHAR(255) NULL DEFAULT '未登録',
    residence VARCHAR(255) NULL DEFAULT '未登録',
    public INTEGER DEFAULT '0' NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
)CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

CREATE TABLE hobby_genres (
    hobby_genre_id VARCHAR(255) PRIMARY KEY,
    hobby_genre_name VARCHAR(50) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
)CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;


CREATE TABLE channels (
    channel_id VARCHAR(255) PRIMARY KEY,
    channel_name VARCHAR(255) NOT NULL,
    channel_comment VARCHAR(255)  NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    user_id  VARCHAR(255) NOT NULL,
    hobby_genre_id VARCHAR(255) NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (hobby_genre_id)
    REFERENCES hobby_genres(hobby_genre_id)
)CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

CREATE TABLE messages (
    message_id VARCHAR(255) PRIMARY KEY,
    message_content TEXT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    channel_id  VARCHAR(255) NOT NULL,
    user_id  VARCHAR(255) NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (channel_id) REFERENCES channels(channel_id) ON DELETE CASCADE
)CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;


CREATE TABLE answers (
    hobby_name_id  VARCHAR(255) PRIMARY KEY ,
    hobby_name VARCHAR(255) NOT NULL,
    total_json_data   JSON NOT NULL,
    class_size INT  NOT NULL
)CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

INSERT INTO users(user_id, email, password, nickname,  icon_image_url) VALUES('970af84c-dd40-47ff-af23-282b72b7cca8','test@gmail.com','5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8','testuser','icon.jpg');


INSERT INTO hobby_genres(hobby_genre_id, hobby_genre_name) VALUES('550e8400-e29b-41d4-a716-446655440000','travel');
INSERT INTO hobby_genres(hobby_genre_id, hobby_genre_name) VALUES('f47ac10b-58cc-4372-a567-0e02b2c3d479','study');
INSERT INTO hobby_genres(hobby_genre_id, hobby_genre_name) VALUES('6ba7b810-9dad-11d1-80b4-00c04fd430c8','movie');
INSERT INTO hobby_genres(hobby_genre_id, hobby_genre_name) VALUES('16fd2706-8baf-433b-82eb-8c7fada847da','comic');
INSERT INTO hobby_genres(hobby_genre_id, hobby_genre_name) VALUES('9b1deb4d-b5a2-4f95-9a4f-5f46f5ee2681','music');
INSERT INTO hobby_genres(hobby_genre_id, hobby_genre_name) VALUES('7c9e6679-7425-40de-944b-e07fc1f90ae7','sauna');
INSERT INTO hobby_genres(hobby_genre_id, hobby_genre_name) VALUES('123e4567-e89b-12d3-a456-426614174000','art');
INSERT INTO hobby_genres(hobby_genre_id, hobby_genre_name) VALUES('3fa85f64-5717-4562-b3fc-2c963f66afa6','muscle');
INSERT INTO hobby_genres(hobby_genre_id, hobby_genre_name) VALUES('b81d2b87-78b5-4b37-8c5c-1e26c3b0c276','sports');
INSERT INTO hobby_genres(hobby_genre_id, hobby_genre_name) VALUES('e3e70682-c209-4cac-629f-6fbed82c07cd','pet');
INSERT INTO hobby_genres(hobby_genre_id, hobby_genre_name) VALUES('5f47ac00-b7cd-4d4d-bdfd-fc09b5f97878','idol');
INSERT INTO hobby_genres(hobby_genre_id, hobby_genre_name) VALUES('a987fbc9-4bed-4078-9f07-9141ba07c9f3','cosme');
INSERT INTO hobby_genres(hobby_genre_id, hobby_genre_name) VALUES('2d931510-d99f-494a-8c67-87feb05e1594','fashion');
INSERT INTO hobby_genres(hobby_genre_id, hobby_genre_name) VALUES('9f8582b4-0ee5-4e69-bfe4-1e8be3e76d6f','relax');
INSERT INTO hobby_genres(hobby_genre_id, hobby_genre_name) VALUES('3bbcee75-cecc-5b56-8031-b6641c1ed1f1','eat');
INSERT INTO hobby_genres(hobby_genre_id, hobby_genre_name) VALUES('21ec2020-3aea-4069-a2dd-08002b30309d','another');


INSERT INTO channels(channel_id, channel_name, user_id, hobby_genre_id) VALUES('c8d1d11e-0f22-4e63-9039-9a8e10b24360','サッカー','970af84c-dd40-47ff-af23-282b72b7cca8','b81d2b87-78b5-4b37-8c5c-1e26c3b0c276');

INSERT INTO messages(message_id, message_content,  channel_id,  user_id) VALUES('91f3f5ab-4bce-4c77-8de7-2b215f6fd1a6','こんにちは！','c8d1d11e-0f22-4e63-9039-9a8e10b24360','970af84c-dd40-47ff-af23-282b72b7cca8');
