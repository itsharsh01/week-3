-- Part D: Ride-sharing schema (sample) + 2 SQL with window functions
-- Run with: sqlite3 < part_d_ride_schema.sql  or open in DB browser

-- Minimal schema
CREATE TABLE IF NOT EXISTS drivers (driver_id INTEGER PRIMARY KEY, name TEXT);
CREATE TABLE IF NOT EXISTS rides (ride_id INTEGER PRIMARY KEY, driver_id INTEGER, rider_id INTEGER, fare REAL, ride_date TEXT);
CREATE TABLE IF NOT EXISTS riders (rider_id INTEGER PRIMARY KEY, name TEXT);

INSERT OR REPLACE INTO drivers VALUES (1,'Ali'),(2,'Bina'),(3,'Carl');
INSERT OR REPLACE INTO riders VALUES (10,'U1'),(20,'U2'),(30,'U3');
INSERT OR REPLACE INTO rides VALUES (101,1,10,50.0,'2025-01-01'),(102,1,20,30.0,'2025-01-02'),(103,2,10,45.0,'2025-01-02'),(104,2,30,60.0,'2025-01-03'),(105,1,30,25.0,'2025-01-03');

-- Query 1: Rides per driver (window: COUNT(*) OVER (PARTITION BY driver_id))
SELECT r.driver_id, d.name,
       COUNT(*) OVER (PARTITION BY r.driver_id) AS ride_count
FROM rides r
JOIN drivers d ON r.driver_id = d.driver_id;

-- Query 2: Rank drivers by total earnings (window: RANK() OVER (ORDER BY total DESC))
SELECT d.driver_id, d.name,
       SUM(r.fare) AS total_earnings,
       RANK() OVER (ORDER BY SUM(r.fare) DESC) AS rank_by_earnings
FROM drivers d
JOIN rides r ON d.driver_id = r.driver_id
GROUP BY d.driver_id, d.name;
