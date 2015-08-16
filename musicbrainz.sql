# CREATE TABLE FOR ARTIST INFORMATION
SELECT x.id, x.name, art_type, g.name AS art_gender, area_id
FROM (
	SELECT a.id, a.name, at.name AS art_type, a.gender, a.area AS area_id
	FROM artist a
	INNER JOIN artist_type at
	ON a.type = at.id) x
LEFT JOIN gender g
ON x.gender = g.id;

# CREATE TABLE FOR LABEL INFORMATION
SELECT la.id, la.name, lt.name AS label_type, la.area AS area_id
FROM label la
LEFT JOIN label_type lt
ON la.type = lt.id;

# CREATE TABLE FOR PLACE INFORMATION
SELECT a.id, a.name, p.id, p.name, p.address, p.coordinates
FROM area a
FULL OUTER JOIN place p
ON p.area = a.id;

# CREATE TABLE FOR RECORDING INFORMATION
SELECT r.id, r.name, r.artist_credit, acn.artist AS art_id
FROM recording r
LEFT JOIN artist_credit_name acn
ON r.artist_credit = acn.artist_credit;

# CREATE TABLE FOR ARTIST TO ARTIST RELATIONSHIP
SELECT x.entity0, x.entity1, lt.name, lt.link_phrase, lt.reverse_link_phrase
FROM (
	SELECT li.link_type, entity0, entity1
	FROM l_artist_artist laa
	LEFT JOIN link li
	ON laa.link = li.id) x
LEFT JOIN link_type lt
ON x.link_type = lt.id
WHERE name = 'collaboration';

# CREATE TABLE FOR ARTIST TO LABEL RELATIONSHIP
SELECT x.entity0, x.entity1, lt.name, lt.link_phrase, lt.reverse_link_phrase
FROM (
	SELECT li.link_type, entity0, entity1
	FROM l_artist_label lal
	LEFT JOIN link li
	ON lal.link = li.id) x
LEFT JOIN link_type lt
ON x.link_type = lt.id
WHERE name = 'recording contract';

# CREATE TABLE FOR ARTIST TO RECORDING RELATIONSHIP
SELECT x.entity0, x.entity1, lt.name, lt.link_phrase, lt.reverse_link_phrase
FROM (
	SELECT li.link_type, entity0, entity1
	FROM l_artist_recording lar
	LEFT JOIN link li
	ON lar.link = li.id) x
LEFT JOIN link_type lt
ON x.link_type = lt.id;

# CREATE TABLE FOR LABEL TO RECORDING RELATIONSHIP
SELECT x.entity0, x.entity1, lt.name, lt.link_phrase, lt.reverse_link_phrase
FROM (
	SELECT li.link_type, entity0, entity1
	FROM l_label_recording llr
	LEFT JOIN link li
	ON llr.link = li.id) x
LEFT JOIN link_type lt
ON x.link_type = lt.id;

# CREATE TABLE FOR PLACE TO RECORDING RELATIONSHIP
SELECT x.entity0, x.entity1, lt.name, lt.link_phrase, lt.reverse_link_phrase
FROM (
	SELECT li.link_type, entity0, entity1
	FROM l_place_recording lpr
	LEFT JOIN link li
	ON lpr.link = li.id) x
LEFT JOIN link_type lt
ON x.link_type = lt.id;

# CREATE TABLE FOR PRODUCER TO LABEL RELATIONSHIP
SELECT x.entity0, x.entity1, lt.name, lt.link_phrase, lt.reverse_link_phrase
FROM (
	SELECT li.link_type, entity0, entity1
	FROM l_artist_label lal
	LEFT JOIN link li
	ON lal.link = li.id) x
LEFT JOIN link_type lt
ON x.link_type = lt.id
WHERE name = 'producer position';

# CREATE TABLE FOR PRODUCER TO RECORDING RELATIONSHIP
SELECT x.entity0, x.entity1, lt.name, lt.link_phrase, lt.reverse_link_phrase
FROM (
	SELECT li.link_type, entity0, entity1
	FROM l_artist_recording lar
	LEFT JOIN link li
	ON lar.link = li.id) x
LEFT JOIN link_type lt
ON x.link_type = lt.id
WHERE name = 'producer';

# CREATE TABLE FOR RECORDING TO RECORDING RELATIONSHIP
SELECT x.entity0, x.entity1, lt.name, lt.link_phrase, lt.reverse_link_phrase
FROM (
	SELECT li.link_type, entity0, entity1
	FROM l_recording_recording lrr
	LEFT JOIN link li
	ON lrr.link = li.id) x
LEFT JOIN link_type lt
ON x.link_type = lt.id;


'''
TERMINAL COMMAND TO SAVE RESULTS FROM MUSICBRAINZ TO FILE:
\COPY (SQL QUERY FROM ABOVE) TO 'filename.csv' WITH CSV;

TERMINAL COMMAND TO GRAB RESULTS FROM MUSICBRAINZ SERVER:
scp - p 2222 vm@localhost:/home/musicbrainz/musicbrainz-server/admin/filename.csv ./

NEED TO DO:

GOOD TO HAVE:
release date
limit to just US?
lyrics
'''
