## Project Overview

This project involves implementing a graph database using Neo4j.
The dataset used is the Nashville Meetup Network: Teaching Dataset for NashNetX Presentation (PyTN).
The project includes the import and modeling of connected datasets into both a relational database (PostgreSQL) and a graph database (Neo4j), followed by querying, performance analysis, and graph analytics.

# Data Import Instructions for Neo4j

This document provides step-by-step instructions for importing data into a Neo4j database using Cypher commands. Follow these steps carefully to ensure that the dataset is properly loaded and indexed.

---

## **Step 1: Prepare Your Environment**

1. **Install Neo4j Desktop:**

   - Download Neo4j Desktop from the [official website](https://neo4j.com/download/).
   - Install and launch Neo4j Desktop.

2. **Create a New Database:**

   - Open Neo4j Desktop.
   - Click on "Add Database" and create a local database.
   - Start the database and open the Neo4j Browser.

3. **Locate the `import` Directory:**

   - Place your dataset files in the Neo4j `import` directory. The path depends on your system:
     - **Windows:** `C:\Users\<your_username>\Neo4j\<database_name>\import`
     - **macOS:** `/Users/<your_username>/Library/Application Support/Neo4j Desktop/Application/relate-data/dbmss/<database_id>/import`
     - **Linux:** `~/.neo4j/<database_name>/import`

4. **Ensure Dataset Files Are Correctly Formatted:**
   - Ensure all `.csv` files are UTF-8 encoded.
   - Verify that each file has a header row matching the column names used in the queries.

---

## **Step 2: Import Data**

Open the Neo4j Browser and execute the following Cypher commands step-by-step.

### **2.1 Import `Member` Nodes**

```cypher
LOAD CSV WITH HEADERS FROM 'file:///meta-members.csv' AS row
CREATE (:Member {member_id: row.member_id, name: row.name, location: row.location});
```

### **2.2 Import `Group` Nodes**

```cypher
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
```

### **2.3 Import `Event` Nodes**

```cypher
LOAD CSV WITH HEADERS FROM 'file:///meta-events.csv' AS row
CREATE (:Event {event_id: row.event_id, name: row.name, time: row.time});
```

---

### **2.4 Create Relationships**

#### **2.4.1 Create `PARTICIPATES_IN` Relationships**

```cypher
LOAD CSV WITH HEADERS FROM 'file:///member-to-group-edges.csv' AS row
MATCH (m:Member {member_id: row.member_id})
MATCH (g:Group {group_id: row.group_id})
CREATE (m)-[:PARTICIPATES_IN {weight: toInteger(row.weight)}]->(g);
```

#### **2.4.2 Create `FRIEND_OF` Relationships**

```cypher
LOAD CSV WITH HEADERS FROM 'file:///member-edges.csv' AS row
MATCH (m1:Member {member_id: row.member1})
MATCH (m2:Member {member_id: row.member2})
WHERE m1 IS NOT NULL AND m2 IS NOT NULL
CREATE (m1)-[:FRIEND_OF {weight: toInteger(row.weight)}]->(m2);
```

#### **2.4.3 Create `CONNECTED_TO` Relationships**

```cypher
LOAD CSV WITH HEADERS FROM 'file:///group-edges.csv' AS row
MATCH (g1:Group {group_id: row.group1})
MATCH (g2:Group {group_id: row.group2})
WHERE g1 IS NOT NULL AND g2 IS NOT NULL
CREATE (g1)-[:CONNECTED_TO {weight: toInteger(row.weight)}]->(g2);
```

#### **2.4.4 Create `ATTENDED` Relationships**

```cypher
LOAD CSV WITH HEADERS FROM 'file:///rsvps.csv' AS row
MATCH (m:Member {member_id: row.member_id})
MATCH (e:Event {event_id: row.event_id})
CREATE (m)-[:ATTENDED]->(e);
```

---

## **Step 3: Create Indexes**

Indexes help improve query performance. Run the following commands to create indexes:

```cypher
CREATE INDEX FOR (m:Member) ON (m.member_id);
CREATE INDEX FOR (g:Group) ON (g.group_id);
CREATE INDEX FOR (g:Group) ON (g.group_name);
CREATE INDEX FOR (e:Event) ON (e.event_id);
```

---

## **Step 4: Verify the Import**

Run the following queries to confirm that the data has been successfully imported:

### **4.1 Verify Node Counts**

```cypher
MATCH (m:Member)
RETURN COUNT(m) AS total_members;

MATCH (g:Group)
RETURN COUNT(g) AS total_groups;

MATCH (e:Event)
RETURN COUNT(e) AS total_events;
```

### **4.2 Verify Relationship Counts**

```cypher
MATCH ()-[r:PARTICIPATES_IN]->()
RETURN COUNT(r) AS total_participates_in;

MATCH ()-[r:FRIEND_OF]->()
RETURN COUNT(r) AS total_friend_of;

MATCH ()-[r:CONNECTED_TO]->()
RETURN COUNT(r) AS total_connected_to;

MATCH ()-[r:ATTENDED]->()
RETURN COUNT(r) AS total_attended;
```

### **4.3 Sample Data Verification**

```cypher
MATCH (m:Member)-[:PARTICIPATES_IN]->(g:Group)
RETURN m.member_id, g.group_name LIMIT 10;

MATCH (m:Member)-[:ATTENDED]->(e:Event)
RETURN m.member_id, e.name LIMIT 10;

MATCH (g1:Group)-[:CONNECTED_TO]->(g2:Group)
RETURN g1.group_name, g2.group_name LIMIT 10;
```

---

## **Notes**

1. Ensure the `file:///` path matches the location of your dataset in the `import` directory.
2. If errors occur during import, verify the CSV file formatting and ensure no missing headers or unexpected data types.

By following these instructions, you will successfully import your dataset into Neo4j and set up your graph database for analysis.
