CREATE DATABASE IF NOT EXISTS stocks;
USE stocks;

CREATE TABLE IF NOT EXISTS `items` (
  `Prod_ID` int NOT NULL,
  `Prod_Name` varchar(25) DEFAULT NULL,
  `num_of_items` int DEFAULT NULL,
  `MRP` int DEFAULT NULL,
  PRIMARY KEY (`Prod_ID`)