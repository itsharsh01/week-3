# Day 15 PM Part D — AI-Augmented Task (Ride-Sharing Schema)

## Prompt used
"Design the database schema for a ride-sharing app (like Ola/Uber). Include ER diagram description, normalised tables, and 5 SQL queries with window functions."

## Documented output
- The AI typically proposes entities: User/Rider, Driver, Ride, Vehicle, Payment, Location, etc., with relationships (User books Ride, Driver assigned, Vehicle linked to Driver, Payment for Ride).
- Normalised tables: Users, Drivers, Vehicles, Rides, Payments, perhaps RideStops or Locations.
- Five SQL queries might include: total rides per driver (window or group by), rank of drivers by earnings, running total of payments per user, etc.

## Evaluation
- **Is the schema in 3NF?** Check that no non-key attribute depends on another non-key attribute. If FDs are stated, we verify that each table’s non-key attributes depend only on the key. Common issues: storing redundant driver name in Rides (should reference Drivers only); storing user name in every Ride (should reference Users). If the AI output has such redundancy, we note “not 3NF” and suggest decomposition.
- **Missing relationships?** E.g. Ride might need explicit link to Pickup and Dropoff locations; Vehicle to Driver (1:1 or N:1); Payment to Ride (1:1). We list any missing relationships we’d add.
- **Run at least 2 SQL queries:** The file **part_d_ride_schema.sql** creates minimal ride-sharing tables (drivers, riders, rides) and runs two SQL queries with window functions: (1) COUNT(*) OVER (PARTITION BY driver_id) for ride count per driver; (2) RANK() OVER (ORDER BY SUM(fare) DESC) for ranking drivers by total earnings. Run with `sqlite3 part_d_ride_schema.sql` to execute; both queries return the expected shape.
