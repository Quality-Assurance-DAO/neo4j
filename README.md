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
                   "actionItems": [
                       {
                           "text": "Action Description",
                           "assignee": "Person Name",
                           "dueDate": "2025-01-14",
                           "status": "todo"
                       }
                   ]
               }
           ]
       }]
   }
   ```

---

## Graph Data Model

### Nodes
- **Meeting**: Contains meeting metadata (workgroup, date, host, topics, emotions)
- **Person**: Represents meeting participants
- **Document**: Working documents referenced in meetings
- **ActionItem**: Tasks assigned during meetings
- **AgendaItem**: Meeting agenda items with status and narrative
- **DiscussionPoint**: Points discussed in agenda items
- **Decision**: Decisions made during the meeting
- **Topic**: Topics covered in the meeting
- **Emotion**: Emotional context or tone of the meeting

### Relationships
- `(Person)-[:ATTENDED]->(Meeting)`
- `(Meeting)-[:HAS_DOCUMENT]->(Document)`
- `(Meeting)-[:HAS_ACTION]->(ActionItem)`
- `(ActionItem)-[:ASSIGNED_TO]->(Person)`
- `(Meeting)-[:HAS_AGENDA_ITEM]->(AgendaItem)`
- `(AgendaItem)-[:INCLUDES_DISCUSSION]->(DiscussionPoint)`
- `(AgendaItem)-[:MADE_DECISION]->(Decision)`
- `(Meeting)-[:COVERS_TOPIC]->(Topic)`
- `(Meeting)-[:HAS_EMOTION]->(Emotion)`

---

## Example Queries

### View Meeting Decisions
```cypher
// View all decisions with full details
MATCH (m:Meeting)-[:MADE_DECISION]->(d:Decision)
RETURN m.date, 
       m.workgroup,
       d.decision as decision_text,
       d.rationale,
       d.opposing,
       d.effect
ORDER BY m.date;

// View decisions that may affect others
MATCH (m:Meeting)-[:MADE_DECISION]->(d:Decision)
WHERE d.effect = 'mayAffectOtherPeople'
RETURN m.date, 
       m.workgroup,
       substring(d.decision, 0, 100) + '...' as decision_preview;

// View decisions for a specific meeting
MATCH (m:Meeting)-[:MADE_DECISION]->(d:Decision)
WHERE m.id = $meeting_id
RETURN m.date, 
       d.decision as decision_text,
       d.rationale,
       d.opposing,
       d.effect;
```

### View Meeting Structure
```cypher
// Basic meeting information with participants
MATCH (p:Person)-[:ATTENDED]->(m:Meeting)
RETURN m.workgroup, m.date, collect(p.name) as participants

// Meeting agenda items and decisions
MATCH (m:Meeting)-[:HAS_AGENDA_ITEM]->(a:AgendaItem)-[:MADE_DECISION]->(d:Decision)
RETURN m.date, a.status, d.decision, d.rationale

// Action items and assignees
MATCH (m:Meeting)-[:HAS_ACTION]->(a:ActionItem)-[:ASSIGNED_TO]->(p:Person)
RETURN m.date, a.text, p.name, a.status, a.dueDate
```

### View Meeting Metadata
```cypher
// Topics covered in meetings
MATCH (m:Meeting)-[:COVERS_TOPIC]->(t:Topic)
RETURN m.date, m.workgroup, collect(t.name) as topics

// Meeting emotions and context
MATCH (m:Meeting)-[:HAS_EMOTION]->(e:Emotion)
RETURN m.date, m.workgroup, collect(e.name) as emotions

// Complete meeting overview
MATCH (m:Meeting)
OPTIONAL MATCH (m)-[:COVERS_TOPIC]->(t:Topic)
OPTIONAL MATCH (m)-[:HAS_EMOTION]->(e:Emotion)
OPTIONAL MATCH (m)-[:MADE_DECISION]->(d:Decision)
RETURN m.date, 
       m.workgroup, 
       collect(DISTINCT t.name) as topics,
       collect(DISTINCT e.name) as emotions,
       count(d) as decisions_made
```

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

