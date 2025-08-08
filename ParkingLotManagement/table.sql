CREATE DATABASE IF NOT EXISTS parking_lot;
USE parking_lot;

CREATE TABLE IF NOT EXISTS parking_slots (
    slot_id INT PRIMARY KEY AUTO_INCREMENT,
    vehicle_number VARCHAR(20),
    vehicle_type VARCHAR(20),
    is_occupied BOOLEAN DEFAULT 0
);
