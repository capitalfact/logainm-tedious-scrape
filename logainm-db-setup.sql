DROP DATABASE logainm;
CREATE DATABASE logainm;
USE logainm;

CREATE TABLE place_name (
	id INT NOT NULL AUTO_INCREMENT,
	en VARCHAR(256) NOT NULL,
	ga VARCHAR(256) NOT NULL,

	PRIMARY KEY (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE place_type (
        id INT NOT NULL AUTO_INCREMENT,
        code VARCHAR(64) NOT NULL UNIQUE,
        description_en VARCHAR(256) NOT NULL,
        description_ga VARCHAR(256) NOT NULL,

        PRIMARY KEY (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE place (
	id INT NOT NULL AUTO_INCREMENT,
	logainm_id INT NOT NULL,
	place_name_id INT NOT NULL,
	place_type_id INT NOT NULL,	
	longitude FLOAT,
	latitude FLOAT,
	geo_accurate BOOLEAN NOT NULL DEFAULT FALSE,

	PRIMARY KEY (id),
	CONSTRAINT FOREIGN KEY (place_type_id) REFERENCES place_type (id),
	CONSTRAINT FOREIGN KEY (place_name_id) REFERENCES place_name (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE place_is_in (
	place_id INT NOT NULL,
	is_in_place_id INT NOT NULL,
	
	CONSTRAINT FOREIGN KEY (place_id) REFERENCES place (id),
	CONSTRAINT FOREIGN KEY (is_in_place_id) REFERENCES place (id),
	CONSTRAINT UK_place_is_in UNIQUE (place_id, is_in_place_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
	
