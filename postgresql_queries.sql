-- sql queries

-- 1. Drop Existing Tables
DROP TABLE IF EXISTS members CASCADE;
DROP TABLE IF EXISTS groups CASCADE;
DROP TABLE IF EXISTS events CASCADE;
DROP TABLE IF EXISTS member_to_group CASCADE;
DROP TABLE IF EXISTS member_edges CASCADE;
DROP TABLE IF EXISTS group_edges CASCADE;
DROP TABLE IF EXISTS rsvps CASCADE;

-- 2. Create New Tables

-- 2.1 Members Table
CREATE TABLE members (
    member_id VARCHAR PRIMARY KEY,
    name VARCHAR,
    hometown VARCHAR,
    city VARCHAR,
    state VARCHAR,
    lat FLOAT,
    lon FLOAT
);

-- 2.2 Groups Table
CREATE TABLE groups (
    group_id VARCHAR PRIMARY KEY,
    group_name VARCHAR,
    num_members INTEGER,
    category_id VARCHAR,
    category_name VARCHAR,
    organizer_id VARCHAR,
    group_urlname VARCHAR
);

-- 2.3 Events Table
CREATE TABLE events (
    event_id VARCHAR PRIMARY KEY,
    group_id VARCHAR REFERENCES groups(group_id),
    name VARCHAR
);

-- 2.4 Member-to-Group Relationships
CREATE TABLE member_to_group (
    member_id VARCHAR REFERENCES members(member_id),
    group_id VARCHAR REFERENCES groups(group_id),
    weight INTEGER
);

-- 2.5 Member-to-Member Relationships
CREATE TABLE member_edges (
    member1 VARCHAR REFERENCES members(member_id),
    member2 VARCHAR REFERENCES members(member_id),
    weight INTEGER
);

-- 2.6 Group-to-Group Relationships
CREATE TABLE group_edges (
    group1 VARCHAR REFERENCES groups(group_id),
    group2 VARCHAR REFERENCES groups(group_id),
    weight INTEGER
);

-- 2.7 RSVPs Table
CREATE TABLE rsvps (
    event_id VARCHAR REFERENCES events(event_id),
    member_id VARCHAR REFERENCES members(member_id),
    group_id VARCHAR REFERENCES groups(group_id)
);

-- 3. Import Data from CSV Files
-- Adjust the file paths accordingly

-- 3.1 Members Table
\COPY members(member_id, name, hometown, city, state, lat, lon) FROM 'C:/datasets/meta-members.csv' WITH CSV HEADER;

-- 3.2 Groups Table
\COPY groups(group_id, group_name, num_members, category_id, category_name, organizer_id, group_urlname) FROM 'C:/datasets/meta-groups.csv' WITH CSV HEADER;

-- 3.3 Events Table
\COPY events(event_id, group_id, name) FROM 'C:/datasets/meta-events.csv' WITH CSV HEADER;

-- 3.4 Member-to-Group Relationships
\COPY member_to_group(member_id, group_id, weight) FROM 'C:/datasets/member-to-group-edges.csv' WITH CSV HEADER;

-- 3.5 Member-to-Member Relationships
\COPY member_edges(member1, member2, weight) FROM 'C:/datasets/member-edges.csv' WITH CSV HEADER;

-- 3.6 Group-to-Group Relationships
\COPY group_edges(group1, group2, weight) FROM 'C:/datasets/group-edges.csv' WITH CSV HEADER;

-- 3.7 RSVPs Table
\COPY rsvps(event_id, member_id, group_id) FROM 'C:/datasets/rsvps.csv' WITH CSV HEADER;

-- 4. Validate the Data
-- Check record counts
SELECT COUNT(*) FROM members;
SELECT COUNT(*) FROM groups;
SELECT COUNT(*) FROM events;

-- Inspect sample data
SELECT * FROM members LIMIT 5;
SELECT * FROM groups LIMIT 5;
SELECT * FROM events LIMIT 5;

-- 6. List All Groups and Their Member Counts
SELECT group_id, group_name, num_members
FROM groups
ORDER BY num_members DESC
LIMIT 10;

-- 7. Find Groups That Are Closely Connected
SELECT g1.group_name AS group1, g2.group_name AS group2, ge.weight
FROM group_edges ge
JOIN groups g1 ON ge.group1 = g1.group_id
JOIN groups g2 ON ge.group2 = g2.group_id
WHERE ge.weight > 10
ORDER BY ge.weight DESC
LIMIT 10;

-- 8. Find Members Attending the Most Events
SELECT m.member_id, COUNT(r.event_id) AS events_attended
FROM members m
JOIN rsvps r ON m.member_id = r.member_id
GROUP BY m.member_id
ORDER BY events_attended DESC
LIMIT 10;

-- 9. Find Members Attending Events in Multiple Groups
SELECT m.member_id, COUNT(DISTINCT g.group_id) AS groups_attended
FROM members m
JOIN member_to_group mtg ON m.member_id = mtg.member_id
JOIN groups g ON mtg.group_id = g.group_id
GROUP BY m.member_id
ORDER BY groups_attended DESC
LIMIT 10;

-- 10. Filter Results After Aggregation
SELECT m.member_id, m.name, COUNT(r.event_id) AS event_count
FROM members m
JOIN rsvps r ON m.member_id = r.member_id
GROUP BY m.member_id, m.name
HAVING COUNT(r.event_id) > 5;

-- 11. Calculate the Total Weight of a Member’s Connections
SELECT m.member_id, SUM(me.weight) AS total_weight
FROM members m
JOIN member_edges me ON m.member_id = me.member1
GROUP BY m.member_id;
