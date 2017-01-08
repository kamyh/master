DROP TABLE IF EXISTS progress;
CREATE TABLE progress (
id int NOT NULL AUTO_INCREMENT,
prot_id varchar(256) DEFAULT NULL,
status int(2) DEFAULT NULL,
PRIMARY KEY (`id`)
);