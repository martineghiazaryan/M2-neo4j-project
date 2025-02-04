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


# PostgreSQL Setup and Queries

## Step 1: Install PostgreSQL
1. Download PostgreSQL from [https://www.postgresql.org/download/](https://www.postgresql.org/download/)
2. Run the installer and follow the steps:
   - **Select components:** Ensure you install `pgAdmin` and `Command Line Tools`.
   - **Set a password:** When prompted, set a password for the default `postgres` user (remember this password).
   - **Set port:** By default, PostgreSQL runs on port `5432` (keep default or change as needed).

---

## Step 2: Start PostgreSQL Server

1. **Open Command Prompt as Administrator** (Windows `Win + X > Command Prompt (Admin)`).
2. Navigate to the PostgreSQL `bin` directory:
   ```cmd
   cd "C:\\Program Files\\PostgreSQL\\17\\bin"
   ```
   _(Replace `17` with your installed PostgreSQL version if different.)_
3. **Start the PostgreSQL server:**
   ```cmd
   pg_ctl -D "C:\\Program Files\\PostgreSQL\\17\\data" start
   ```
   - If you see a message like `server started`, PostgreSQL is running.
   - If you get an error about the database already running, check for existing processes.

---

## Step 3: Stop PostgreSQL Server (If Needed)

To stop the running PostgreSQL service, use:
```cmd
pg_ctl -D "C:\\Program Files\\PostgreSQL\\17\\data" stop
```

---

## Step 4: Connect to PostgreSQL Using `psql`

1. Open **Command Prompt** and navigate to PostgreSQL `bin` directory:
   ```cmd
   cd "C:\\Program Files\\PostgreSQL\\17\\bin"
   ```
2. Connect to PostgreSQL with the default user:
   ```cmd
   psql -U postgres
   ```
   - If prompted, enter the password you set during installation.
   - If you see the PostgreSQL prompt (`postgres=#`), the connection is successful.

---

## Step 5: Create and Connect to the `meetup_graph` Database

1. **Create the database:**
   ```sql
   CREATE DATABASE meetup_graph;
   ```
2. **Connect to the database:**
   ```cmd
   \c meetup_graph
   ```
   You should see: `You are now connected to database "meetup_graph"`.

---

## Step 6: Execute SQL Queries

Once inside PostgreSQL (`meetup_graph=#` prompt), run your queries step by step:

```sql
DROP TABLE IF EXISTS members CASCADE;
DROP TABLE IF EXISTS groups CASCADE;
DROP TABLE IF EXISTS events CASCADE;
DROP TABLE IF EXISTS member_to_group CASCADE;
DROP TABLE IF EXISTS member_edges CASCADE;
DROP TABLE IF EXISTS group_edges CASCADE;
DROP TABLE IF EXISTS rsvps CASCADE;
```

```sql
CREATE TABLE members (
    member_id VARCHAR PRIMARY KEY,
    name VARCHAR,
    hometown VARCHAR,
    city VARCHAR,
    state VARCHAR,
    lat FLOAT,
    lon FLOAT
);
```

```sql
CREATE TABLE groups (
    group_id VARCHAR PRIMARY KEY,
    group_name VARCHAR,
    num_members INTEGER,
    category_id VARCHAR,
    category_name VARCHAR,
    organizer_id VARCHAR,
    group_urlname VARCHAR
);
```

```sql
CREATE TABLE events (
    event_id VARCHAR PRIMARY KEY,
    group_id VARCHAR REFERENCES groups(group_id),
    name VARCHAR
);
```

```sql
CREATE TABLE member_to_group (
    member_id VARCHAR REFERENCES members(member_id),
    group_id VARCHAR REFERENCES groups(group_id),
    weight INTEGER
);
```

```sql
CREATE TABLE member_edges (
    member1 VARCHAR REFERENCES members(member_id),
    member2 VARCHAR REFERENCES members(member_id),
    weight INTEGER
);
```

```sql
CREATE TABLE group_edges (
    group1 VARCHAR REFERENCES groups(group_id),
    group2 VARCHAR REFERENCES groups(group_id),
    weight INTEGER
);
```

```sql
CREATE TABLE rsvps (
    event_id VARCHAR REFERENCES events(event_id),
    member_id VARCHAR REFERENCES members(member_id),
    group_id VARCHAR REFERENCES groups(group_id)
);
```

---

## Step 7: Import Data from CSV Files

```sql
\COPY members(member_id, name, hometown, city, state, lat, lon) FROM 'datasets/meta-members.csv' WITH CSV HEADER;
```

```sql
\COPY groups(group_id, group_name, num_members, category_id, category_name, organizer_id, group_urlname) FROM 'datasets/meta-groups.csv' WITH CSV HEADER;
```

```sql
\COPY events(event_id, group_id, name) FROM 'datasets/meta-events.csv' WITH CSV HEADER;
```

```sql
\COPY member_to_group(member_id, group_id, weight) FROM 'datasets/member-to-group-edges.csv' WITH CSV HEADER;
```

```sql
\COPY member_edges(member1, member2, weight) FROM 'datasets/member-edges.csv' WITH CSV HEADER;
```

```sql
\COPY group_edges(group1, group2, weight) FROM 'datasets/group-edges.csv' WITH CSV HEADER;
```

```sql
\COPY rsvps(event_id, member_id, group_id) FROM 'datasets/rsvps.csv' WITH CSV HEADER;
```

---

## Step 8: Validate the Data

```sql
SELECT COUNT(*) FROM members;
SELECT COUNT(*) FROM groups;
SELECT COUNT(*) FROM events;
```

```sql
SELECT * FROM members LIMIT 5;
SELECT * FROM groups LIMIT 5;
SELECT * FROM events LIMIT 5;
```

# **GraphRAG-powered Neo4j Query System**

## **Getting Started**
This repository provides a **GraphRAG-powered Neo4j query system** that allows users to **query Neo4j using natural language** and receive structured results in **JSON and tabular formats** via a **Gradio UI**.

---

## **Setup & Installation**

### **1️⃣ Install Dependencies**
Ensure you have **Python 3.10+** installed. Then, clone the repository and install the required packages:

```bash
git clone <repo>
cd graphRAG
pip install -r requirements.txt
```

### **2️⃣ Configure Neo4j Connection**
- Make sure you have **Neo4j installed** and running.
- Update your **config.py** file with your **Neo4j database credentials**:

```python
NEO4J_URI = "bolt://localhost:7687"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "your_password"
```

### **3️⃣ Configure OpenAI API Key**
- Add your **OpenAI API Key** inside a `.env` file:

```bash
OPENAI_API_KEY="your_openai_api_key"
OPENAI_MODEL="gpt-4o-mini"
```

---

## **▶Running the Application**
To launch the Gradio UI, simply run:

```bash
python main.py
```

You should see an output similar to:

```bash
Running on local URL:  http://127.0.0.1:7860
```

Open this link in your browser to access the **GraphRAG-powered UI**.

---

## **How to Use**
1️⃣ **Enter a natural language query** in the input field.  
   Example:  
   ```plaintext
   Show me all members who have attended at least one event.
   ```
   
2️⃣ Click **"Submit"** to process the query.  

3️⃣ The system will:
   - Convert the natural language query to a **Cypher query**.
   - Run the Cypher query on **Neo4j**.
   - Display the **JSON output** (structured result).
   - Generate a **formatted table** of the results.

4️⃣ Click **"Clear"** to reset the UI.

---

### **🔹 Basic Queries**
1️⃣ **"List all members in the database."**  
2️⃣ **"Show me all groups available in the network."**  
3️⃣ **"Find all events that have taken place."**  
4️⃣ **"Who are the organizers of each group?"**  
5️⃣ **"Get all friendships between members."**  

---

### **🔹 Filtering Queries**
6️⃣ **"Show me all members who have attended at least one event."**  
7️⃣ **"Find all groups that have more than 500 members."**  
8️⃣ **"List all events that happened in the last 6 months."**  
9️⃣ **"Show groups that are related to Tech or Business categories."**  
🔟 **"Find all members who have participated in at least 3 groups."**  

---

### **🔹 Relationship-Based Queries**
1️⃣1️⃣ **"Which members are friends with each other?"**  
1️⃣2️⃣ **"Show me members who have attended the same event."**  
1️⃣3️⃣ **"Find members who have participated in multiple groups together."**  
1️⃣4️⃣ **"Get a list of members who are organizers of a group and also attend events."**  
1️⃣5️⃣ **"Find groups that have overlapping members."**  

---

### **🔹 Advanced Queries**
1️⃣6️⃣ **"Which group has the most members?"**  
1️⃣7️⃣ **"Show me the top 5 most attended events."**  
1️⃣8️⃣ **"Find the most connected member based on friendships."**  
1️⃣9️⃣ **"List groups with similar categories to 'Sports & Recreation'."**  
2️⃣0️⃣ **"Which events had the highest attendance?"**  

---

### **🔹 Complex Queries**
2️⃣1️⃣ **"Find members who attended a Tech-related event and also belong to a Business group."**  
2️⃣2️⃣ **"List groups where at least 50% of members have attended an event."**  


## **Troubleshooting**
**1️⃣ Gradio UI does not start?**  
- Ensure **Neo4j is running** and your **config.py** credentials are correct.

**2️⃣ No results found?**  
- The dataset may not contain matching nodes. Try a **different query**.

**3️⃣ OpenAI errors?**  
- Ensure your **API key** is valid and has sufficient quota.

