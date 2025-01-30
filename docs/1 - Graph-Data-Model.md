The graph data model represents meetings and their associated components in a structured format. Each entity within the system plays a key role in capturing essential meeting details, participant interactions, and decision-making processes.

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
Relationships define how the various entities within the meeting structure interact with each other. The following relationships establish meaningful connections:

- `(Person)-[:ATTENDED]->(Meeting)`
- `(Meeting)-[:HAS_DOCUMENT]->(Document)`
- `(Meeting)-[:HAS_AGENDA_ITEM]->(AgendaItem)`
- `(AgendaItem)-[:HAS_ACTION]->(ActionItem)`
- `(ActionItem)-[:ASSIGNED_TO]->(Person)`
- `(AgendaItem)-[:INCLUDES_DISCUSSION]->(DiscussionPoint)`
- `(AgendaItem)-[:MADE_DECISION]->(Decision)`
- `(Meeting)-[:COVERS_TOPIC]->(Topic)`
- `(Meeting)-[:HAS_EMOTION]->(Emotion)`

## Example Queries
The following Cypher queries help extract meaningful insights from the meeting graph:

### View Action Items with Meeting Context
This query retrieves all action items assigned in meetings, along with details about the responsible individuals and the due dates:

```cypher
// View action items with their meeting context
MATCH (m:Meeting)-[:HAS_ACTION]->(act:ActionItem)-[:ASSIGNED_TO]->(p:Person)
RETURN m.date,
       m.workgroup,
       act.text as action,
       p.name as assignee,
       act.dueDate,
       act.status;
```

### Alternative View Including Agenda Items
This query enhances the previous one by optionally including agenda items when available:

```cypher
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

To get a comprehensive view of the entire meeting structure, the following query extracts all relationships connected to meetings:

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
```

### Overview with Numerical Counts
This query provides a high-level statistical summary of meeting-related entities:

```cypher
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

The first query provides a full graph visualization, allowing users to explore the structure in detail.
The second query summarizes the relationships numerically, helping to understand the volume of actions, decisions, topics, and attendees per meeting.
This structured data model enables efficient querying, analysis, and insights into meeting-related interactions, making it easier to track participation, monitor action items, and analyze decision-making patterns.