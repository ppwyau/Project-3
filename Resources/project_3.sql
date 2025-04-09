drop table road_accident_data

CREATE TABLE road_accident_data (
	accident_index VARCHAR,
	accident_date DATE,
	"month" VARCHAR,
	"day_of_week" VARCHAR,
	year INT,
	junction_control VARCHAR, 
	junction_detail VARCHAR,
	accident_severity VARCHAR,
	latitude DOUBLE PRECISION,
	light_conditions VARCHAR,
	local_authority VARCHAR,
	carriageway_hazards VARCHAR,
	longitude DOUBLE PRECISION, 
	number_of_casualties INT, 
	number_of_vehicles INT, 
	police_force VARCHAR,
	road_surface_conditions VARCHAR,
	road_type VARCHAR, 
	speed_limit INT,
	"time" TIME,
	urban_or_rural_area VARCHAR,
	weather_conditions VARCHAR,
	vehicle_type VARCHAR
);

SELECT * FROM road_accident_data