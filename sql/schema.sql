DROP TABLE IF EXISTS login_activity;
DROP TABLE IF EXISTS hospitals;

CREATE TABLE hospitals (
    hospital_id INT PRIMARY KEY AUTO_INCREMENT,
    hospital_name VARCHAR(255),
    address VARCHAR(255),
    city VARCHAR(255),
    state VARCHAR(255),
    zip_code VARCHAR(10),
    county_name VARCHAR(255),
    phone_number VARCHAR(20),
    hospital_type VARCHAR(255),
    hospital_ownership VARCHAR(255),
    latitude DECIMAL(10, 8),
    longitude DECIMAL(11, 8)
);

CREATE TABLE login_activity (
    id INT PRIMARY KEY AUTO_INCREMENT,
    hospital_id INT,
    login_count INT,
    signin_provider_id INT,
    FOREIGN KEY (hospital_id) REFERENCES hospitals(hospital_id)
);