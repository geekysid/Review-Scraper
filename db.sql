-- source table
CREATE TABLE m2websolution_db.tb_source (
	source_id int auto_increment NOT NULL,
	source_name varchar(100) NOT NULL,
	active bool DEFAULT True NOT NULL,
	CONSTRAINT tb_source_PK PRIMARY KEY (source_id),
	CONSTRAINT tb_source_UN UNIQUE KEY (source_name)
)
ENGINE=InnoDB
DEFAULT CHARSET=utf8mb4
COLLATE=utf8mb4_0900_ai_ci;

-- status table
CREATE TABLE m2websolution_db.tb_status (
	status_id int auto_increment NOT NULL,
	status varchar(100) NOT NULL,
	description text NULL,
	CONSTRAINT tb_stauts_PK PRIMARY KEY (status_id),
	CONSTRAINT tb_stauts_UN UNIQUE KEY (status)
)
ENGINE=InnoDB
DEFAULT CHARSET=utf8mb4
COLLATE=utf8mb4_0900_ai_ci;

-- job table
CREATE TABLE m2websolution_db.tb_jobs (
	job_id int auto_increment NOT NULL,
	url varchar(500) NOT NULL,
	source varchar(100) NOT NULL,
	reviews_from_date timestamp DEFAULT '2020-01-01 00:00:00' NULL,
	reviews_to_date timestamp DEFAULT CURRENT_TIMESTAMP NULL,
	status varchar(100) NOT NULL,
	execution_start_date timestamp NULL,
	execution_end_date timestamp NULL,
	date_added timestamp DEFAULT CURRENT_TIMESTAMP NULL,
	last_updated timestamp NULL,
	remarks text NULL,
	CONSTRAINT tb_jobs_PK PRIMARY KEY (job_id),
	CONSTRAINT tb_jobs_UN UNIQUE KEY (url,reviews_from_date,reviews_to_date),
	CONSTRAINT tb_jobs_FK FOREIGN KEY (source) REFERENCES m2websolution_db.tb_source(source_name) ON DELETE RESTRICT ON UPDATE RESTRICT,
	-- CONSTRAINT tb_jobs_FK_1 FOREIGN KEY (status) REFERENCES m2websolution_db.tb_stauts(status) ON DELETE RESTRICT ON UPDATE RESTRICT
)
ENGINE=InnoDB
DEFAULT CHARSET=utf8mb4
COLLATE=utf8mb4_0900_ai_ci;

-- logs table
CREATE TABLE m2websolution_db.tb_logs (
	id int auto_increment NOT NULL,
	job_id int NOT NULL,
	file_name varchar(500) NOT NULL,
	path_to_file text NOT NULL,
	url_to_file text NULL,
	date_added timestamp DEFAULT CURRENT_TIMESTAMP NULL,
	CONSTRAINT tb_logs_PK PRIMARY KEY (id),
	CONSTRAINT tb_logs_UN UNIQUE KEY (file_name),
	CONSTRAINT tb_logs_FK FOREIGN KEY (job_id) REFERENCES m2websolution_db.tb_jobs(job_id) ON DELETE CASCADE ON UPDATE CASCADE
)
ENGINE=InnoDB
DEFAULT CHARSET=utf8mb4
COLLATE=utf8mb4_0900_ai_ci;


-- tripdvisor review table
CREATE TABLE m2websolution_db.tb_tripadvisor_reviews (
  id int NOT NULL AUTO_INCREMENT,
  job_id int NOT NULL,
  published_date varchar(50) DEFAULT NULL,
  rating double DEFAULT NULL,
  text text,
  title varchar(100) DEFAULT NULL,
  username varchar(100) DEFAULT NULL,
  user_info varchar(100) DEFAULT NULL,
  publish_platform varchar(100) DEFAULT NULL,
  provider_name varchar(100) DEFAULT NULL,
  trip_info json DEFAULT NULL,
  social_statistics json DEFAULT NULL,
  owner_response json DEFAULT NULL,
  hash varchar(500) NOT NULL,
  scraped_date timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  tripadvisor_id int DEFAULT NULL,
  PRIMARY KEY (id),
  UNIQUE KEY tb_reviews_UN (hash),
  KEY tb_reviews_FK (job_id),
  CONSTRAINT tb_reviews_FK FOREIGN KEY (job_id) REFERENCES tb_jobs (job_id) ON DELETE RESTRICT ON UPDATE RESTRICT
);


-- trustpilot review table
CREATE TABLE m2websolution_db.tb_trustpilot_reviews (
  id int NOT NULL AUTO_INCREMENT,
  job_id int NOT NULL,
  trustpilot_id varchar(50) DEFAULT NULL,
  published_date varchar(50) DEFAULT NULL,
  rating double DEFAULT NULL,
  text text,
  title text,
  likes varchar(100) DEFAULT NULL,
  consumer_name varchar(100) DEFAULT NULL,
  user_info json DEFAULT NULL,
  reply json DEFAULT NULL,
  hash varchar(500) NOT NULL,
  scraped_date timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  UNIQUE KEY tb_trustpilot_reviews_UN (hash),
  KEY tb_trustpilot_reviews_FK (job_id),
  CONSTRAINT tb_trustpilot_FK FOREIGN KEY (job_id) REFERENCES tb_jobs (job_id) ON DELETE RESTRICT ON UPDATE RESTRICT
);


-- booking review table
CREATE TABLE m2websolution_db.tb_booking_reviews (
  id int NOT NULL AUTO_INCREMENT,
  job_id int NOT NULL,
  published_date varchar(50) DEFAULT NULL,
  reviewer_name varchar(50) DEFAULT NULL,
  reviewer_country varchar(50) DEFAULT NULL,
  room_type varchar(50) DEFAULT NULL,
  stay_duration varchar(50) DEFAULT NULL,
  stay_date varchar(50) DEFAULT NULL,
  title text,
  like_comment text,
  dislike_comment text,
  hotel_response text,
  rating double DEFAULT NULL,
  likes varchar(100) DEFAULT NULL,
  user_info json DEFAULT NULL,
  hash varchar(500) NOT NULL,
  scraped_date timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  UNIQUE KEY tb_booking_reviews_UN (hash),
  KEY tb_booking_reviews_FK (job_id),
  CONSTRAINT tb_booking_FK FOREIGN KEY (job_id) REFERENCES tb_jobs (job_id) ON DELETE RESTRICT ON UPDATE RESTRICT
);



-- INSERT INTO tb_source (source_name, active) VALUES ('tripadvisor.com', true);
-- INSERT INTO tb_source (source_name, active) VALUES ('trustpilot.com', true);
-- INSERT INTO tb_source (source_name, active) VALUES ('booking.com', true);

-- INSERT INTO tb_status (status, description) VALUES ('ADDED', 'Job was created');
-- INSERT INTO tb_status (status, description) VALUES ('QUEUED', 'Job Added to the Queue');
-- INSERT INTO tb_status (status, description) VALUES ('RUNNING', 'Job is currently executng');
-- INSERT INTO tb_status (status, description) VALUES ('ERRORED', 'Job threw an error and terminated');
-- INSERT INTO tb_status (status, description) VALUES ('COMPLETED', 'Job executed successfully');
-- INSERT INTO tb_status (status, description) VALUES ('CANCELED', 'Job was canceled');
-- INSERT INTO tb_status (status, description) VALUES ('EXCEPTION', 'Job thew an exception and terminated');
