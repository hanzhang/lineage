#######################################
###		Setting Up SQL Tables 		###
#######################################

# DEFINING TABLES
CREATE TABLE artist_data
(id integer, name varchar, type varchar, gender varchar,
area_id integer);

CREATE TABLE recording_data
(id integer, name varchar, artist_credit integer,
art_id integer);

CREATE TABLE label_data
(id integer, name varchar, label_type varchar,
area_id integer);

CREATE TABLE place_data
(area_id integer, area_name varchar, place_id integer,
place_name varchar, place_address varchar, place_coordinates varchar);

CREATE TABLE artist_to_artist
(entity0 integer, entity1 integer, link_name varchar, 
link_phrase varchar, reverse_link_phrase varchar);

CREATE TABLE artist_to_label
(entity0 integer, entity1 integer, link_name varchar, 
link_phrase varchar, reverse_link_phrase varchar);

CREATE TABLE artist_to_recording 
(entity0 integer, entity1 integer, link_name varchar, 
link_phrase varchar, reverse_link_phrase varchar);

CREATE TABLE label_to_recording 
(entity0 integer, entity1 integer, link_name varchar, 
link_phrase varchar, reverse_link_phrase varchar);

CREATE TABLE producer_to_label
(entity0 integer, entity1 integer, link_name varchar, 
link_phrase varchar, reverse_link_phrase varchar);

CREATE TABLE producer_to_recording
(entity0 integer, entity1 integer, link_name varchar,
link_phrase varchar, reverse_link_phrase varchar);

CREATE TABLE recording_to_recording 
(entity0 integer, entity1 integer, link_name varchar, 
link_phrase varchar, reverse_link_phrase varchar);


#######################################
###		Importing From CSVs 		###
#######################################

\copy artist_data(id, name, type, gender, area_id) FROM 'Desktop/Han/lineage/data/artist_data.csv' DELIMITER ',' CSV;
\copy recording_data(id, name, artist_credit, art_id) FROM 'Desktop/Han/lineage/data/recording_data.csv' DELIMITER ',' CSV;
\copy label_data(id, name, label_type, area_id) FROM 'Desktop/Han/lineage/data/label_data.csv' DELIMITER ',' CSV;
\copy place_data(area_id, area_name, place_id, place_name, place_address, place_coordinates) FROM 'Desktop/Han/lineage/data/place_data.csv' DELIMITER ',' CSV;
\copy artist_to_artist(entity0, entity1, link_name, link_phrase, reverse_link_phrase) FROM 'Desktop/Han/lineage/data/artist_to_artist.csv' DELIMITER ',' CSV;
\copy artist_to_label(entity0, entity1, link_name, link_phrase, reverse_link_phrase) FROM 'Desktop/Han/lineage/data/artist_to_label.csv' DELIMITER ',' CSV;
\copy artist_to_recording(entity0, entity1, link_name, link_phrase, reverse_link_phrase) FROM 'Desktop/Han/lineage/data/artist_to_recording.csv' DELIMITER ',' CSV;
\copy label_to_recording(entity0, entity1, link_name, link_phrase, reverse_link_phrase) FROM 'Desktop/Han/lineage/data/label_to_recording.csv' DELIMITER ',' CSV;
\copy producer_to_label(entity0, entity1, link_name, link_phrase, reverse_link_phrase) FROM 'Desktop/Han/lineage/data/producer_to_label.csv' DELIMITER ',' CSV;
\copy producer_to_recording(entity0, entity1, link_name, link_phrase, reverse_link_phrase) FROM 'Desktop/Han/lineage/data/producer_to_recording.csv' DELIMITER ',' CSV;
\copy recording_to_recording(entity0, entity1, link_name, link_phrase, reverse_link_phrase) FROM 'Desktop/Han/lineage/data/recording_to_recording.csv' DELIMITER ',' CSV;


#######################################
###		Creating Graph Edges 		###
#######################################

# CREATE ARTIST TO ARTIST TABLE FOR GRAPH
SELECT *
INTO artist_to_artist_edges
FROM (
	SELECT ('art' || CAST(entity0 AS varchar)) AS artist1, ('art' || CAST(entity1 AS varchar)) AS artist2, 'artist_to_artist' AS connection_type FROM artist_to_artist
	UNION
	SELECT ('art' || CAST(entity1 AS varchar)) AS artist1, ('art' || CAST(entity0 AS varchar)) AS artist2, 'artist_to_artist' AS connection_type FROM artist_to_artist) x;

# CREATE ARTIST TO LABEL TABLE FOR GRAPH
SELECT *
INTO artist_to_label_edges
FROM (
	WITH t1 AS (
		SELECT ('art' || CAST(artist1 AS varchar)) AS artist1, ('lab' || CAST(label2 AS varchar)) AS label2, 'artist_to_label' AS connection_type
		FROM (
			SELECT r.art_id AS artist1, ltr.entity0 AS label2
			FROM recording_data r
			INNER JOIN label_to_recording ltr
			ON r.id = ltr.entity1) x
		GROUP BY artist1, label2
		UNION
		SELECT ('art' || CAST(entity0 AS varchar)) AS artist1, ('lab' || CAST(entity1 AS varchar)) AS label2, 'artist_to_label' AS connection_type FROM artist_to_label)
	SELECT artist1, label2, connection_type FROM t1
	UNION
	SELECT label2, artist1, connection_type FROM t1) y;

# CREATE ARTIST TO RECORDING TABLE FOR GRAPH
SELECT *
INTO artist_to_recording_edges
FROM (
	SELECT ('art' || CAST(art_id AS varchar)) AS artist1, ('rec' || CAST(id AS varchar)) AS recording2, 'artist_to_recording' AS connection_type FROM recording_data
	UNION
	SELECT ('rec' || CAST(id AS varchar)) AS artist1, ('art' || CAST(art_id AS varchar)) AS recording2, 'artist_to_recording' AS connection_type FROM recording_data) x;

# CREATE LABEL TO RECORDING TABLE FOR GRAPH
SELECT *
INTO label_to_recording_edges
FROM (
	SELECT ('lab' || CAST(entity0 AS varchar)) AS label1, ('rec' || CAST(entity1 AS varchar)) AS recording2, 'label_to_recording' AS connection_type FROM label_to_recording
	UNION
	SELECT ('rec' || CAST(entity1 AS varchar)) AS label1, ('lab' || CAST(entity0 AS varchar)) AS recording2, 'label_to_recording' AS connection_type FROM label_to_recording) x;

# CREATE PRODUCER TO LABEL TABLE FOR GRAPH
SELECT *
INTO producer_to_label_edges
FROM (
	WITH t1 AS (
		SELECT ('pro' || CAST(producer1 AS varchar)) AS producer1, ('lab' || CAST(label2 AS varchar)) AS label2, 'producer_to_label' AS connection_type
		FROM (
			SELECT ptr.entity0 AS producer1, ltr.entity0 AS label2
			FROM producer_to_recording ptr
			INNER JOIN label_to_recording ltr
			ON ptr.entity1 = ltr.entity1) x
		GROUP BY producer1, label2
		UNION
		SELECT ('pro' || CAST(entity0 AS varchar)) AS producer1, ('lab' || CAST(entity1 AS varchar)) AS label2, 'producer_to_label' AS connection_type FROM producer_to_label)
	SELECT producer1, label2, connection_type FROM t1
	UNION
	SELECT label2, producer1, connection_type FROM t1) y;

# CREATE PRODUCER TO RECORDING TABLE FOR GRAPH
SELECT *
INTO producer_to_recording_edges
FROM (
	SELECT ('pro' || CAST(entity0 AS varchar)) AS producer1, ('rec' || CAST(entity1 AS varchar)) AS recording2, 'producer_to_recording' AS connection_type FROM producer_to_recording
	UNION
	SELECT ('rec' || CAST(entity1 AS varchar)) AS producer1, ('pro' || CAST(entity0 AS varchar)) AS recording2, 'producer_to_recording' AS connection_type FROM producer_to_recording) x;

# CREATE RECORDING TO RECORDING TABLE FOR GRAPH
SELECT *
INTO recording_to_recording_edges
FROM (
	SELECT ('rec' || CAST(entity0 AS varchar)) AS recording1, ('rec' || CAST(entity1 AS varchar)) AS recording2, 'recording_to_recording' AS connection_type FROM recording_to_recording
	UNION
	SELECT ('rec' || CAST(entity1 AS varchar)) AS recording1, ('rec' || CAST(entity0 AS varchar)) AS recording2, 'recording_to_recording' AS connection_type FROM recording_to_recording) x;

# CREATE PRODUCER TO ARTIST TABLE FOR GRAPH
SELECT *
INTO producer_to_artist_edges
FROM (
	WITH t1 AS(
		SELECT ('pro' || CAST(entity0 AS varchar)) AS producer1, ('art' || CAST(art_id AS varchar)) AS artist2, 'producer_to_artist'::text AS connection_type
		FROM producer_to_recording ptr
		INNER JOIN recording_data r
		ON ptr.entity1 = r.id)
	SELECT producer1, artist2, connection_type FROM t1
	UNION
	SELECT artist2, producer1, connection_type FROM t1) x;


#######################################
###		Creating Graph Nodes 		###
#######################################

# CREATE ARTIST NODES
SELECT *
INTO artist_nodes
FROM (
	WITH all_artists AS (
		SELECT ('art' || CAST(id AS varchar)) AS node_id, name AS node_name, 'artist'::text AS node_type
		FROM artist_data)
	SELECT node_id, node_name, node_type
	FROM all_artists
	INNER JOIN (
		SELECT artist1 AS id FROM artist_to_artist_edges WHERE artist1 LIKE 'art%'
		UNION
		SELECT artist1 AS id FROM artist_to_recording_edges WHERE artist1 LIKE 'art%'
		UNION
		SELECT artist1 AS id FROM artist_to_label_edges WHERE artist1 LIKE 'art%'
		UNION
		SELECT artist2 AS id FROM producer_to_artist_edges WHERE artist2 LIKE 'art%') x
	ON node_id = x.id) y;

# CREATE LABEL NODES
SELECT *
INTO label_nodes
FROM (
	WITH all_labels AS (
		SELECT ('lab' || CAST(id AS varchar)) AS node_id, name AS node_name, 'label'::text AS node_type
		FROM artist_data)
	SELECT node_id, node_name, node_type
	FROM all_labels
	INNER JOIN (
		SELECT label2 AS id FROM artist_to_label_edges WHERE label2 LIKE 'lab%'
		UNION
		SELECT label1 AS id FROM label_to_recording_edges WHERE label1 LIKE 'lab%'
		UNION
		SELECT label2 AS id FROM producer_to_label_edges WHERE label2 LIKE 'lab%') x
	ON node_id = x.id) y;

# CREATE PRODUCER NODES
SELECT *
INTO producer_nodes
FROM (
	WITH all_producers AS (
		SELECT ('pro' || CAST(id AS varchar)) AS node_id, name AS node_name, 'producer'::text AS node_type
		FROM artist_data)
	SELECT node_id, node_name, node_type
	FROM all_producers
	INNER JOIN (
		SELECT producer1 AS id FROM producer_to_label_edges WHERE producer1 LIKE 'pro%'
		UNION
		SELECT producer1 AS id FROM producer_to_recording_edges WHERE producer1 LIKE 'pro%'
		UNION
		SELECT producer1 AS id FROM producer_to_artist_edges WHERE producer1 LIKE 'pro%') x
	ON node_id = x.id) y;

# CREATE RECORDING NODES
SELECT *
INTO recording_nodes
FROM (
	WITH all_recordings AS (
		SELECT ('rec' || CAST(id AS varchar)) AS node_id, name AS node_name, 'recording'::text AS node_type
		FROM artist_data)
	SELECT node_id, node_name, node_type
	FROM all_recordings
	INNER JOIN (
		SELECT recording2 AS id FROM artist_to_recording_edges WHERE recording2 LIKE 'rec%'
		UNION
		SELECT recording2 AS id FROM label_to_recording_edges WHERE recording2 LIKE 'rec%'
		UNION
		SELECT recording2 AS id FROM producer_to_recording_edges WHERE recording2 LIKE 'rec%'
		UNION
		SELECT recording1 AS id FROM recording_to_recording_edges WHERE recording1 LIKE 'rec%') x
	ON node_id = x.id) y;


#######################################
###		Aggregating Graph Edges		###
#######################################

SELECT *
INTO all_graph_edges
FROM (
	SELECT * FROM artist_to_artist_edges
	UNION
	SELECT * FROM artist_to_label_edges
	UNION
	SELECT * FROM artist_to_recording_edges
	UNION
	SELECT * FROM label_to_recording_edges
	UNION
	SELECT * FROM producer_to_label_edges
	UNION
	SELECT * FROM producer_to_recording_edges
	UNION
	SELECT * FROM recording_to_recording_edges
	UNION
	SELECT * FROM producer_to_artist_edges) x;


#######################################
###		Aggregating Graph Nodes		###
#######################################

SELECT *
INTO all_graph_nodes
FROM (
	SELECT * FROM artist_nodes
	UNION
	SELECT * FROM label_nodes
	UNION
	SELECT * FROM producer_nodes
	UNION
	SELECT * FROM recording_nodes) x;

'''
JUST IN CASE, CONVERT LABELS:
ALTER TABLE artist_nodes ALTER COLUMN node_type TYPE text;
ALTER TABLE label_nodes ALTER COLUMN node_type TYPE text;
ALTER TABLE producer_nodes ALTER COLUMN node_type TYPE text;
ALTER TABLE recording_nodes ALTER COLUMN node_type TYPE text;


SAVE GRAPH LABELS AND NODES:
\COPY all_graph_xx TO 'all_graph_xx.csv' DELIMITER ',' CSV HEADER;
'''
