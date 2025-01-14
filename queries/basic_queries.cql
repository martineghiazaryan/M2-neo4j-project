// Find members without attended events
MATCH (m:Member)
OPTIONAL MATCH (m)-[:ATTENDED]->(e:Event)
WHERE e IS NULL
RETURN m.member_id, m.name;

// Find all members and include their attended events
MATCH (m:Member)
OPTIONAL MATCH (m)-[:ATTENDED]->(e:Event)
RETURN m.member_id, m.name, e.event_id;

// Filter members who attended more than 5 events
MATCH (m:Member)-[:ATTENDED]->(e:Event)
WITH m, COUNT(e) AS event_count
WHERE event_count > 5
RETURN m.member_id, m.name, event_count;

// Group members by the number of events attended
MATCH (m:Member)-[:ATTENDED]->(e:Event)
WITH m, COLLECT(e.name) AS events
RETURN m.name, events;

// Calculate the total weight of a member’s connections
MATCH (m:Member)-[r:FRIEND_OF]->(:Member)
RETURN m.member_id, REDUCE(total = 0, rel IN COLLECT(r) | total + rel.weight) AS total_weight;

// List all groups and their member counts
MATCH (g:Group)
RETURN g.group_id, g.group_name, g.num_members
ORDER BY g.num_members DESC LIMIT 10;

// Find all members who belong to a specific group
MATCH (m:Member)-[:PARTICIPATES_IN]->(g:Group {group_id: "339011"})
RETURN m.member_id, m.name;

// Find members attending the most events
MATCH (m:Member)-[:ATTENDED]->(e:Event)
RETURN m.member_id, COUNT(e) AS events_attended
ORDER BY events_attended DESC LIMIT 10;

// Visualize members and their groups
MATCH (m:Member)-[:PARTICIPATES_IN]->(g:Group)
RETURN m, g
LIMIT 10;

// Visualize the group connection network
MATCH (g1:Group)-[r:CONNECTED_TO]->(g2:Group)
RETURN g1, g2, r
LIMIT 10;

// View a specific relationship between members and groups
MATCH (m:Member)-[r:PARTICIPATES_IN]->(g:Group)
RETURN m, r, g LIMIT 10;