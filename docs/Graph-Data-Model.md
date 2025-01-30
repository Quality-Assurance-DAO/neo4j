
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

## Example Queries
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