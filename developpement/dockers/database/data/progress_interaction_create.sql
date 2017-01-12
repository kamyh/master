DROP TABLE IF EXISTS progress_interaction;
CREATE TABLE progress_interaction (
id int NOT NULL AUTO_INCREMENT,
interaction_id int(11) DEFAULT NULL,
status int(2) DEFAULT NULL,
PRIMARY KEY (`id`)
);