## Understanding Node Degree

Node Degree is a fundamental metric in graph analysis that measures how connected a node is. Think of it as counting a node's relationships.

```cypher
// Basic Node Degree Analysis
MATCH (n)
OPTIONAL MATCH (n)-->(out)
OPTIONAL MATCH (n)<--(in)
OPTIONAL MATCH (n)--(total)
RETURN 
    labels(n)[0] as NodeType,
    CASE labels(n)[0]
        WHEN 'Person' THEN n.name
        WHEN 'Meeting' THEN n.workgroup + ' (' + n.date + ')'
        ELSE coalesce(n.title, n.text, '')
    END as NodeName,
    count(DISTINCT out) as OutDegree,   // Outgoing relationships
    count(DISTINCT in) as InDegree,     // Incoming relationships
    count(DISTINCT total) as TotalDegree // All relationships
ORDER BY TotalDegree DESC;
```

### Types of Degree:

1. **Out-Degree**
   - Number of outgoing relationships
   - Example: Person -[ATTENDED]-> Meeting
   - Shows: How many meetings a person attended

2. **In-Degree**
   - Number of incoming relationships
   - Example: Meeting <-[ATTENDED]- Person
   - Shows: How many people attended a meeting

3. **Total Degree**
   - Total number of relationships (both directions)
   - Shows: Overall connectivity of a node

### Real-World Examples:

```cypher
// Example: Meeting Attendance Degree
MATCH (m:Meeting)
OPTIONAL MATCH (m)<-[att:ATTENDED]-(p:Person)
OPTIONAL MATCH (m)-[act:HAS_ACTION]->(a:ActionItem)
RETURN 
    m.workgroup + ' (' + m.date + ')' as Meeting,
    count(DISTINCT p) as Attendees,      // In-Degree for ATTENDED
    count(DISTINCT a) as ActionItems,    // Out-Degree for HAS_ACTION
    count(DISTINCT p) + count(DISTINCT a) as TotalConnections
ORDER BY TotalConnections DESC;

// Example: Person Activity Degree
MATCH (p:Person)
OPTIONAL MATCH (p)-[att:ATTENDED]->(m:Meeting)
OPTIONAL MATCH (p)<-[assigned:ASSIGNED_TO]-(a:ActionItem)
RETURN 
    p.name as Person,
    count(DISTINCT m) as MeetingsAttended,    // Out-Degree for ATTENDED
    count(DISTINCT a) as AssignedActions,     // In-Degree for ASSIGNED_TO
    count(DISTINCT m) + count(DISTINCT a) as TotalActivity
ORDER BY TotalActivity DESC;
```

### Significance:

1. **High Degree Nodes**
   - Meetings with many attendees
   - People involved in many meetings
   - Topics discussed frequently

2. **Low Degree Nodes**
   - One-off meetings
   - Occasional participants
   - Rarely discussed topics

3. **Business Insights**
   - Identify key participants
   - Find important meetings
   - Discover central topics