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
	date_last_updated timestamp NULL,
	remarks text NULL,
	CONSTRAINT tb_jobs_PK PRIMARY KEY (job_id),
	CONSTRAINT tb_jobs_UN UNIQUE KEY (url,reviews_from_date,reviews_to_date),
	CONSTRAINT tb_jobs_FK FOREIGN KEY (source) REFERENCES m2websolution_db.tb_source(source_name) ON DELETE RESTRICT ON UPDATE RESTRICT,
	-- CONSTRAINT tb_jobs_FK_1 FOREIGN KEY (status) REFERENCES m2websolution_db.tb_stauts(status) ON DELETE RESTRICT ON UPDATE RESTRICT
)
ENGINE=InnoDB
DEFAULT CHARSET=utf8mb4
COLLATE=utf8mb4_0900_ai_ci;

-- review table
CREATE TABLE m2websolution_db.tb_tripadvisor_reviews (
	id int auto_increment NOT NULL,
	job_id int NOT NULL,
	published_date varchar(50) NULL,
	rating DOUBLE NULL,
	`text` text NULL,
	title varchar(100) NULL,
	username varchar(100) NULL,
	user_info varchar(100) NULL,
	publish_platform varchar(100) NULL,
	provider_name varchar(100) NULL,
	trip_info json NULL,
	social_statistics json NULL,
	owner_response json NULL,
	hash varchar(500) NOT NULL,
	scraped_data timestamp DEFAULT CURRENT_TIMESTAMP NOT NULL,
	CONSTRAINT tb_reviews_PK PRIMARY KEY (id),
	CONSTRAINT tb_reviews_UN UNIQUE KEY (hash),
	CONSTRAINT tb_reviews_FK FOREIGN KEY (job_id) REFERENCES m2websolution_db.tb_jobs(job_id) ON DELETE RESTRICT ON UPDATE RESTRICT
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

