// Load Member nodes
LOAD CSV WITH HEADERS FROM 'file:///meta-members.csv' AS row
CREATE (:Member {member_id: row.member_id, name: row.name, location: row.location});

// Load Group nodes
LOAD CSV WITH HEADERS FROM 'file:///meta-groups.csv' AS row
CREATE (:Group {
  group_id: row.group_id,
  group_name: row.group_name,
  num_members: toInteger(row.num_members),
  category_id: row.category_id,
  category_name: row.category_name,
  organizer_id: row.organizer_id,
  group_urlname: row.group_urlname
});

// Load Event nodes
LOAD CSV WITH HEADERS FROM 'file:///meta-events.csv' AS row
CREATE (:Event {event_id: row.event_id, name: row.name, time: row.time});

// Create PARTICIPATES_IN relationships
LOAD CSV WITH HEADERS FROM 'file:///member-to-group-edges.csv' AS row
MATCH (m:Member {member_id: row.member_id})
MATCH (g:Group {group_id: row.group_id})
CREATE (m)-[:PARTICIPATES_IN {weight: toInteger(row.weight)}]->(g);

// Create indexes for optimization
CREATE INDEX FOR (m:Member) ON (m.member_id);
CREATE INDEX FOR (g:Group) ON (g.group_id);
CREATE INDEX FOR (g:Group) ON (g.group_name);
CREATE INDEX FOR (e:Event) ON (e.event_id);

// Create FRIEND_OF relationships
LOAD CSV WITH HEADERS FROM 'file:///member-edges.csv' AS row
MATCH (m1:Member {member_id: row.member1})
MATCH (m2:Member {member_id: row.member2})
WHERE m1 IS NOT NULL AND m2 IS NOT NULL
CREATE (m1)-[:FRIEND_OF {weight: toInteger(row.weight)}]->(m2);

// Create CONNECTED_TO relationships
LOAD CSV WITH HEADERS FROM 'file:///group-edges.csv' AS row
MATCH (g1:Group {group_id: row.group1})
MATCH (g2:Group {group_id: row.group2})
WHERE g1 IS NOT NULL AND g2 IS NOT NULL
CREATE (g1)-[:CONNECTED_TO {weight: toInteger(row.weight)}]->(g2);

// Create ATTENDED relationships
LOAD CSV WITH HEADERS FROM 'file:///rsvps.csv' AS row
MATCH (m:Member {member_id: row.member_id})
MATCH (e:Event {event_id: row.event_id})
CREATE (m)-[:ATTENDED]->(e);
