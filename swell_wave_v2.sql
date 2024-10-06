CREATE DATABASE IF NOT EXISTS swell_wave_v2;
USE swell_wave_v2;

-- Table to store location data
CREATE TABLE IF NOT EXISTS locations (
    location_id INT PRIMARY KEY AUTO_INCREMENT,
    latitude DECIMAL(10, 7) NOT NULL,
    longitude DECIMAL(10, 7) NOT NULL,
    elevation DECIMAL(5, 2),
    location_name VARCHAR(100)
);

-- Table to store unit data
CREATE TABLE IF NOT EXISTS units (
    unit_id INT PRIMARY KEY AUTO_INCREMENT,
    time_unit VARCHAR(50),
    interval_unit VARCHAR(50),
    swell_wave_height_unit VARCHAR(50),
    swell_wave_direction_unit VARCHAR(50),
    swell_wave_period_unit VARCHAR(50)
);

-- Table to store current swell data
CREATE TABLE IF NOT EXISTS current_swell (
    current_swell_id INT PRIMARY KEY AUTO_INCREMENT,
    location_id INT NOT NULL,
    time DATETIME NOT NULL,
    swell_wave_height DECIMAL(5, 2) NOT NULL,
    swell_wave_direction DECIMAL(5, 2),
    swell_wave_period DECIMAL(5, 2),
    FOREIGN KEY (location_id) REFERENCES locations(location_id)
);

-- Table to store hourly swell data
CREATE TABLE IF NOT EXISTS hourly_swell (
    hourly_swell_id INT PRIMARY KEY AUTO_INCREMENT,
    location_id INT NOT NULL,
    time DATETIME NOT NULL,
    swell_wave_height DECIMAL(5, 2) NOT NULL,
    swell_wave_direction DECIMAL(5, 2),
    swell_wave_period DECIMAL(5, 2),
    FOREIGN KEY (location_id) REFERENCES locations(location_id)
);
