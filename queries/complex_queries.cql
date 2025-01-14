// Find groups that are closely connected (high weight)
MATCH (g1:Group)-[r:CONNECTED_TO]->(g2:Group)
WHERE r.weight > 10
RETURN g1.group_name, g2.group_name, r.weight
ORDER BY r.weight DESC LIMIT 10;

// Find members attending events in multiple groups
MATCH (m:Member)-[:PARTICIPATES_IN]->(g:Group)
MATCH (m)-[:ATTENDED]->(e:Event)
RETURN m.member_id, COUNT(DISTINCT g.group_id) AS groups_attended
ORDER BY groups_attended DESC LIMIT 10;

// Identify highly connected groups (degree centrality)
MATCH (g:Group)-[:CONNECTED_TO]-()
RETURN g.group_name, COUNT(*) AS connections
ORDER BY connections DESC LIMIT 10;

// Find members who share common groups
MATCH (m1:Member)
WITH m1
LIMIT 1000  // Process 1000 members at a time
MATCH (m1)-[:PARTICIPATES_IN]->(g:Group)<-[:PARTICIPATES_IN]-(m2:Member)
WHERE m1 <> m2
RETURN m1.member_id, m2.member_id, COUNT(DISTINCT g.group_id) AS common_groups
ORDER BY common_groups DESC LIMIT 10;

// Find events that all members in a group attended
MATCH (g:Group {group_name: "Code for Nashville"})<-[:PARTICIPATES_IN]-(m:Member)
MATCH (m)-[:ATTENDED]->(e:Event)
WITH g, e, COLLECT(DISTINCT m.member_id) AS attendees
MATCH (g)<-[:PARTICIPATES_IN]-(allMembers:Member)
WITH e, attendees, COLLECT(DISTINCT allMembers.member_id) AS allGroupMembers
WHERE apoc.coll.containsAll(allGroupMembers, attendees)
RETURN e.event_id, e.name;

// Find members with the highest weighted friendships
MATCH (m1:Member)-[r:FRIEND_OF]->(m2:Member)
RETURN m1.member_id, m2.member_id, SUM(r.weight) AS total_weight
ORDER BY total_weight DESC LIMIT 10;

// Recommend events for members based on their groups
MATCH (m1:Member)-[:PARTICIPATES_IN]->(g:Group)<-[:PARTICIPATES_IN]-(m2:Member)
WHERE m1 <> m2 AND NOT EXISTS {
  MATCH (m1)-[:FRIEND_OF]-(m2)
}
WITH m1, m2, COUNT(DISTINCT g) AS shared_groups
WHERE shared_groups > 0
RETURN m1.member_id, m2.member_id, shared_groups
ORDER BY shared_groups DESC LIMIT 10;

// Recommend friends based on shared groups
MATCH (m1:Member)-[:PARTICIPATES_IN]->(g:Group)<-[:PARTICIPATES_IN]-(m2:Member)
WHERE m1 <> m2 AND NOT (m1)-[:FRIEND_OF]-(m2)
RETURN m1.member_id, m2.member_id, COUNT(g) AS shared_groups
ORDER BY shared_groups DESC LIMIT 10;
