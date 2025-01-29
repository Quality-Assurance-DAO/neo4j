# SingularityNET Meeting Data Graph Database

[![Python](https://img.shields.io/badge/Python-3.8+-blue?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org)
[![Neo4j](https://img.shields.io/badge/Neo4j-4.4+-blue?style=for-the-badge&logo=neo4j&logoColor=white)](https://neo4j.com)
[![Made with Cursor](https://img.shields.io/badge/Made%20with-Cursor-blue?style=for-the-badge&logo=cursor&logoColor=white)](https://cursor.sh)
[![License](https://img.shields.io/badge/License-MIT-green.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)
[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg?style=for-the-badge)](https://github.com/username/repository/graphs/commit-activity)

## Overview

This utility imports SingularityNET meeting data into a Neo4j Aura graph database, creating a queryable graph structure of meetings, participants, documents, action items, and metadata.

## Data Model Visualization

![Graph Data Model](graph-model.png)

*Figure 1: Graph model showing relationships between Meetings and related entities*

---

## Features

- **Meeting Data Import**: Converts JSON meeting data into a graph structure
- **Graph Relationships**: Creates connections between meetings, people, documents, and tasks
- **Environment Variable Configuration**: Securely loads Neo4j credentials from `.env`
- **Error Handling**: Comprehensive error logging for troubleshooting

---

## Prerequisites

- Python 3.8 or later
- Neo4j Aura database instance
- Required Python packages:
  ```bash
  pip install neo4j python-dotenv
  ```

---

## Setup

1. **Clone and Configure**:
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. **Create `.env` File**:
   ```ini
   NEO4J_URI=neo4j+s://<your-database-uri>
   NEO4J_USERNAME=neo4j
   NEO4J_PASSWORD=<your-password>
   ```

3. **Prepare Meeting Data**:
   Place your meeting data in `snet-data.json` following this structure:
   ```json
   {
       "meeting_id": [{
           "workgroup": "Governance Workgroup",
           "meetingInfo": {
               "name": "Weekly",
               "date": "2025-01-07",
               "host": "Host Name",
               "documenter": "Documenter Name",
               "peoplePresent": "Person1, Person2, Person3",
               "purpose": "Meeting Purpose",
               "workingDocs": [
                   {"title": "Doc Title", "link": "Doc URL"}
               ]
           },
           "agendaItems": [
               {
                   "status": "carry over",
                   "narrative": "Discussion narrative...",
                   "actionItems": [
                       {
                           "text": "Action Description",
                           "assignee": "Person Name",
                           "dueDate": "2025-01-14",
                           "status": "todo"
                       }
                   ],
                   "decisionItems": [
                       {
                           "decision": "Decision description",
                           "rationale": "Reasoning behind decision",
                           "opposing": "none",
                           "effect": "affectsOnlyThisWorkgroup"
                       }
                   ],
                   "discussionPoints": [
                       "Point 1",
                       "Point 2"
                   ]
               }
           ],
           "tags": {
               "topicsCovered": "Topic1, Topic2, Topic3",
               "emotions": "Productive, Collaborative"
           }
       }]
   }
   ```

---

## Graph Data Model

### Nodes
- **Meeting**: Contains meeting metadata (workgroup, date, host, topics, emotions)
- **Person**: Represents meeting participants
- **Document**: Working documents referenced in meetings
- **AgendaItem**: Meeting agenda items with status and narrative
- **ActionItem**: Tasks assigned during meetings
- **DiscussionPoint**: Points discussed in agenda items
- **Decision**: Decisions made during the meeting
- **Topic**: Topics covered in the meeting
- **Emotion**: Emotional context or tone of the meeting

### Relationships
- `(Person)-[:ATTENDED]->(Meeting)`
- `(Meeting)-[:HAS_DOCUMENT]->(Document)`
- `(Meeting)-[:HAS_AGENDA_ITEM]->(AgendaItem)`
- `(AgendaItem)-[:HAS_ACTION]->(ActionItem)`
- `(ActionItem)-[:ASSIGNED_TO]->(Person)`
- `(AgendaItem)-[:INCLUDES_DISCUSSION]->(DiscussionPoint)`
- `(AgendaItem)-[:MADE_DECISION]->(Decision)`
- `(Meeting)-[:COVERS_TOPIC]->(Topic)`
- `(Meeting)-[:HAS_EMOTION]->(Emotion)`

### Example Queries
```cypher
// View action items with their meeting context
MATCH (m:Meeting)-[:HAS_ACTION]->(act:ActionItem)-[:ASSIGNED_TO]->(p:Person)
RETURN m.date,
       m.workgroup,
       act.text as action,
       p.name as assignee,
       act.dueDate,
       act.status;

// Alternative view including agenda items when available
MATCH (m:Meeting)
OPTIONAL MATCH (m)-[:HAS_ACTION]->(act:ActionItem)-[:ASSIGNED_TO]->(p:Person)
RETURN m.date,
       m.workgroup,
       collect({
           action: act.text,
           assignee: p.name,
           dueDate: act.dueDate,
           status: act.status
       }) as actions;
```

### Graph Overview Query
```cypher
// Get a complete view of the meeting graph structure
MATCH (m:Meeting)
OPTIONAL MATCH (m)-[r1:HAS_ACTION]->(act:ActionItem)-[r2:ASSIGNED_TO]->(p:Person)
OPTIONAL MATCH (m)-[r3:HAS_DOCUMENT]->(d:Document)
OPTIONAL MATCH (m)-[r4:MADE_DECISION]->(dec:Decision)
OPTIONAL MATCH (m)-[r5:COVERS_TOPIC]->(t:Topic)
OPTIONAL MATCH (m)-[r6:HAS_EMOTION]->(e:Emotion)
OPTIONAL MATCH (att:Person)-[r7:ATTENDED]->(m)
RETURN *;

// Overview with correct counting syntax
MATCH (m:Meeting)
OPTIONAL MATCH (m)-[:HAS_ACTION]->(a:ActionItem)
OPTIONAL MATCH (m)-[:MADE_DECISION]->(d:Decision)
OPTIONAL MATCH (m)-[:COVERS_TOPIC]->(t:Topic)
OPTIONAL MATCH (p:Person)-[:ATTENDED]->(m)
OPTIONAL MATCH (m)-[:HAS_DOCUMENT]->(doc:Document)
RETURN m.date,
       m.workgroup,
       count(DISTINCT a) as action_count,
       count(DISTINCT d) as decision_count,
       count(DISTINCT t) as topic_count,
       count(DISTINCT p) as attendee_count,
       count(DISTINCT doc) as document_count
ORDER BY m.date DESC;
```

The first query visualizes the complete graph structure, while the second query provides a numerical overview of all connected entities for each meeting.

### Graph Structure Analysis

#### 1. Node Label Analysis
```cypher
// Basic node count by label
MATCH (n)
RETURN distinct labels(n) as Node_Type,
       count(*) as Count
ORDER BY Count DESC;

// Nodes with their properties
MATCH (n)
WITH labels(n)[0] as Node_Type, 
     collect(DISTINCT keys(n)) as Properties,
     count(*) as Count
RETURN Node_Type,
       Properties,
       Count
ORDER BY Count DESC;

// Isolated nodes (nodes without relationships)
MATCH (n)
WHERE NOT (n)--()
RETURN labels(n) as Node_Type,
       count(*) as Isolated_Count;
```

#### 2. Relationship Analysis
```cypher
// Direct relationships between node types
MATCH (a)-[r]->(b)
RETURN DISTINCT
    labels(a)[0] as Source_Type,
    type(r) as Relationship,
    labels(b)[0] as Target_Type,
    count(*) as Frequency
ORDER BY Frequency DESC;

// Meeting-centric relationships
MATCH (m:Meeting)
OPTIONAL MATCH (m)-[r]->(target)
RETURN DISTINCT
    type(r) as Relationship_Type,
    labels(target)[0] as Connected_To,
    count(*) as Connection_Count
ORDER BY Connection_Count DESC;

// Person interactions
MATCH (p:Person)
OPTIONAL MATCH (p)-[r]-(connected)
RETURN DISTINCT
    type(r) as Relationship_Type,
    labels(connected)[0] as Connected_To,
    count(*) as Interaction_Count,
    collect(DISTINCT p.name)[0..5] as Sample_People
ORDER BY Interaction_Count DESC;
```

#### 3. Graph Schema
```cypher
// Complete graph schema
CALL db.schema.visualization();

// Custom schema view
MATCH (a)-[r]->(b)
WITH labels(a)[0] as Source_Label,
     type(r) as Relationship_Type,
     labels(b)[0] as Target_Label,
     count(*) as Frequency,
     collect(DISTINCT keys(a)) as Source_Properties,
     collect(DISTINCT keys(b)) as Target_Properties
RETURN Source_Label,
       Source_Properties,
       Relationship_Type,
       Target_Label,
       Target_Properties,
       Frequency
ORDER BY Source_Label, Relationship_Type;

// Property analysis
MATCH (n)
WITH labels(n)[0] as Node_Type,
     keys(n) as Properties
UNWIND Properties as Property
RETURN DISTINCT
    Node_Type,
    collect(DISTINCT Property) as Property_Keys,
    count(DISTINCT Property) as Property_Count
ORDER BY Node_Type;
```

These queries provide:
1. **Label Analysis**:
   - Basic node counts
   - Property analysis for each node type
   - Detection of isolated nodes

2. **Relationship Analysis**:
   - Direct connections between different node types
   - Meeting-centric view of relationships
   - Person interaction patterns

3. **Schema Information**:
   - Built-in schema visualization
   - Custom schema view with properties
   - Property key analysis

Use these queries to understand:
- Data distribution across node types
- Connection patterns
- Data model completeness
- Potential anomalies or isolated data

### Specialized Graph Analysis

#### 1. Node-Specific Queries
```cypher
// Meeting Analysis
MATCH (m:Meeting)
OPTIONAL MATCH (p:Person)-[:ATTENDED]->(m)
WITH m.workgroup as workgroup,
     m.date as meeting_date,
     count(DISTINCT p) as attendee_count
RETURN workgroup,
       count(*) as meeting_count,
       min(meeting_date) as first_meeting,
       max(meeting_date) as last_meeting,
       avg(attendee_count) as avg_attendance
ORDER BY meeting_count DESC;

// Alternative detailed view
MATCH (m:Meeting)
OPTIONAL MATCH (p:Person)-[:ATTENDED]->(m)
RETURN m.workgroup as workgroup,
       m.date as meeting_date,
       count(DISTINCT p) as attendee_count,
       collect(p.name) as attendees
ORDER BY m.date DESC;
```

#### 2. Temporal Analysis
```cypher
// Meeting Frequency Over Time
MATCH (m:Meeting)
WITH date(m.date) as meeting_date,
     m.workgroup as workgroup
RETURN workgroup,
       meeting_date.quarter as quarter,
       meeting_date.year as year,
       count(*) as meeting_count
ORDER BY year, quarter;

// Decision Timeline
MATCH (m:Meeting)-[:MADE_DECISION]->(d:Decision)
WITH date(m.date) as decision_date,
     d.effect as effect_type,
     count(*) as decision_count
RETURN decision_date,
       effect_type,
       decision_count
ORDER BY decision_date;

// Action Item Tracking
MATCH (m:Meeting)-[:HAS_ACTION]->(a:ActionItem)
WHERE a.dueDate IS NOT NULL
WITH a.dueDate as original_date,
     a.status as status
RETURN original_date as due_date,
       status,
       count(*) as action_count
ORDER BY original_date;

// Action Items with Status Distribution
MATCH (m:Meeting)-[:HAS_ACTION]->(a:ActionItem)
RETURN a.status as status,
       count(*) as action_count,
       collect(a.dueDate) as due_dates
ORDER BY action_count DESC;

// Action Items by Meeting
MATCH (m:Meeting)-[:HAS_ACTION]->(a:ActionItem)
RETURN m.date as meeting_date,
       count(*) as action_count,
       collect({
           text: a.text,
           status: a.status,
           dueDate: a.dueDate
       }) as actions
ORDER BY m.date DESC;
```

#### 3. Data Quality Checks
```cypher
// Missing Required Properties
MATCH (m:Meeting)
WHERE m.date IS NULL 
   OR m.workgroup IS NULL
   OR m.host IS NULL
RETURN 'Meeting' as Node_Type,
       m.id as ID,
       [k in keys(m) WHERE m[k] IS NULL] as Null_Properties;

// Comprehensive Property Check
MATCH (n)
WITH n, labels(n)[0] as Node_Type
WITH n, Node_Type,
     CASE Node_Type
         WHEN 'Meeting' THEN ['date', 'workgroup', 'host']
         WHEN 'Person' THEN ['name']
         WHEN 'ActionItem' THEN ['text', 'status', 'assignee']
         WHEN 'Decision' THEN ['decision', 'effect']
         ELSE []
     END as required_properties
WITH n, Node_Type, required_properties,
     [prop in required_properties WHERE n[prop] IS NULL] as missing_properties
WHERE size(missing_properties) > 0
RETURN Node_Type,
       n.id as ID,
       missing_properties,
       properties(n) as existing_properties;

// Empty String Properties
MATCH (n)
WITH n, labels(n)[0] as Node_Type,
     [k in keys(n) WHERE n[k] = ''] as empty_properties
WHERE size(empty_properties) > 0
RETURN Node_Type,
       n.id as ID,
       empty_properties;
```

These queries help you:

1. **Node-Specific Analysis**:
   - Track meeting patterns by workgroup
   - Monitor participant engagement
   - Analyze document usage

2. **Temporal Analysis**:
   - View meeting frequency trends
   - Track decision-making patterns
   - Monitor action item timelines

3. **Data Quality**:
   - Find missing required properties
   - Identify orphaned nodes
   - Detect date format issues
   - Find potential duplicates
   - Check relationship integrity

Use these queries to:
- Monitor participation patterns
- Track workgroup activity
- Identify data quality issues
- Ensure data consistency

---

## Usage

Run the importer:
```bash
python neo.py
```

### Example Queries

View all relationships:
```cypher
MATCH (n)-[r]->(m)
RETURN n, r, m
```

Show meetings and participants:
```cypher
MATCH (p:Person)-[:ATTENDED]->(m:Meeting)
RETURN m.workgroup, m.date, collect(p.name) as participants
```

View action items and assignees:
```cypher
MATCH (m:Meeting)-[:HAS_ACTION]->(a:ActionItem)-[:ASSIGNED_TO]->(p:Person)
RETURN m.date, a.text, p.name, a.status, a.dueDate
```

View meeting structure:
```cypher
MATCH (p:Person)-[:ATTENDED]->(m:Meeting)
RETURN m.workgroup, m.date, collect(p.name) as participants
```

View meeting agenda items and decisions:
```cypher
MATCH (m:Meeting)-[:HAS_AGENDA_ITEM]->(a:AgendaItem)-[:MADE_DECISION]->(d:Decision)
RETURN m.date, a.status, d.decision, d.rationale
```

View meeting metadata:
```cypher
MATCH (m:Meeting)-[:COVERS_TOPIC]->(t:Topic)
RETURN m.date, m.workgroup, collect(t.name) as topics

MATCH (m:Meeting)-[:HAS_EMOTION]->(e:Emotion)
RETURN m.date, m.workgroup, collect(e.name) as emotions

MATCH (m:Meeting)
OPTIONAL MATCH (m)-[:COVERS_TOPIC]->(t:Topic)
OPTIONAL MATCH (m)-[:HAS_EMOTION]->(e:Emotion)
RETURN m.date, m.workgroup, 
       collect(DISTINCT t.name) as topics,
       collect(DISTINCT e.name) as emotions
```

---

## Files
- `neo.py`: Database connection and data import logic
- `snet-data.json`: Source meeting data
- `.env`: Neo4j credentials (not tracked in git)
- `.gitignore`: Git ignore rules

---

## Notes

- Ensure `.env` is in `.gitignore` to protect credentials
- Meeting data should follow the specified JSON structure
- Requires active Neo4j Aura instance

---

## License

MIT License

---

