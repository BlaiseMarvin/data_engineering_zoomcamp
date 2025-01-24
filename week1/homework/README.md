# Homework

## Question One
Code used to get answer:
- docker run -it python:3.12.8 bash
- pip --version
- **Answer: pip 24.3.1**

## Question 2
Code used to get to answer:
- docker-compose -f qn2_docker-compose.yml up -d
- for which we connect the db server using host name db and port 5432
- **this was really obvious by looking at the compose file really, can verify it without needing to run the services**

## Question 3
Code used to get answer:
- ingestion.ipynb notebook

code:
Query1
```
SELECT
	COUNT(*)
FROM green_taxi_data
WHERE lpep_dropoff_datetime >= '2019-10-01' AND lpep_dropoff_datetime < '2019-11-01' AND trip_distance <= 1
```

Query2:
```
SELECT
	COUNT(*)
FROM green_taxi_data
WHERE (lpep_dropoff_datetime >= '2019-10-01' AND lpep_dropoff_datetime < '2019-11-01') AND trip_distance > 1 AND trip_distance <= 3
```

Query3
```
SELECT
	COUNT(*)
FROM green_taxi_data
WHERE (lpep_dropoff_datetime >= '2019-10-01' AND lpep_dropoff_datetime < '2019-11-01') AND trip_distance > 3 AND trip_distance <= 7
```
Query4
```
SELECT
	COUNT(*)
FROM green_taxi_data
WHERE (lpep_dropoff_datetime >= '2019-10-01' AND lpep_dropoff_datetime < '2019-11-01') AND trip_distance > 7 AND trip_distance <= 10
```

Query 5
```
SELECT
	COUNT(*)
FROM green_taxi_data
WHERE (lpep_dropoff_datetime >= '2019-10-01' AND lpep_dropoff_datetime < '2019-11-01') AND trip_distance > 10
```

## Question 4:
Pick up day with the longest trip distance: SQL code:
```
SELECT
	lpep_pickup_datetime
FROM green_taxi_data
WHERE trip_distance = (SELECT MAX(trip_distance) FROM green_taxi_data)
```

## Question 5:
Here is the code:
Disclaimer - my top 3 are East Harlem North, East Harlem South and Central Harlem. Just gonna pick the closest answer for this one
```
SELECT
	"Zone",
	SUM(gt.total_amount) AS "total"
FROM green_taxi_data gt
JOIN zones z
ON ("PULocationID" = "LocationID")
GROUP BY "PULocationID","Zone"
ORDER BY SUM(gt.total_amount) DESC
```

## Question 6:
Here is the code that gives JFK Airport as the answer:
```
SELECT "Zone"
FROM zones
WHERE "LocationID" = (
                        SELECT
                            "DOLocationID"
                        FROM green_taxi_data
                        JOIN zones
                        ON ("PULocationID"="LocationID")
                        WHERE "Zone"='East Harlem North' AND lpep_pickup_datetime BETWEEN '2019-10-01' AND '2019-10-31'
                        ORDER BY tip_amount DESC
                        LIMIT 1
                        )
```

