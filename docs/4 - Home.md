

## Relationship Definitions

1. **Person -> Meeting**
   - `ATTENDED`: Indicates a person was present at a meeting
   - Direction: Person to Meeting
   - Example: `(Person {name: 'John'}) -[:ATTENDED]-> (Meeting {date: '2025-01-01'})`

2. **Meeting -> ActionItem**
   - `HAS_ACTION`: Links a meeting to tasks or actions decided during the meeting
   - Direction: Meeting to ActionItem
   - Example: `(Meeting) -[:HAS_ACTION]-> (ActionItem {text: 'Review proposal'})`

3. **ActionItem -> Person**
   - `ASSIGNED_TO`: Shows who is responsible for completing an action item
   - Direction: ActionItem to Person
   - Example: `(ActionItem {text: 'Review'}) -[:ASSIGNED_TO]-> (Person {name: 'Jane'})`

4. **Meeting -> Document**
   - `HAS_DOCUMENT`: Links a meeting to its related documents
   - Direction: Meeting to Document
   - Example: `(Meeting) -[:HAS_DOCUMENT]-> (Document {title: 'Proposal v1'})`

5. **Meeting -> Decision**
   - `MADE_DECISION`: Connects a meeting to decisions made during it
   - Direction: Meeting to Decision
   - Example: `(Meeting) -[:MADE_DECISION]-> (Decision {decision: 'Approved proposal'})`

6. **Meeting -> Topic**
   - `COVERS_TOPIC`: Shows topics discussed in a meeting
   - Direction: Meeting to Topic
   - Example: `(Meeting) -[:COVERS_TOPIC]-> (Topic {name: 'Governance'})`

7. **Meeting -> Emotion**
   - `HAS_EMOTION`: Indicates the emotional context or tone of a meeting
   - Direction: Meeting to Emotion
   - Example: `(Meeting) -[:HAS_EMOTION]-> (Emotion {name: 'Productive'})`

### Key Points:
- All relationships are directed (one-way)
- Meetings are the central node type, connecting to most other nodes
- Action Items create a chain from Meeting through Action to Person
- Topics and Emotions provide context and categorization
- Documents track meeting materials and references

## Graph Metrics Relationships

```cypher
// 1. Degree and Path Length
MATCH (n)
OPTIONAL MATCH (n)-[r]-(neighbor)
WITH n, 
     count(DISTINCT neighbor) as degree,
     labels(n)[0] as nodeType
MATCH path = (n)-[*1..3]-(connected)
WITH n, nodeType, degree, connected, path
RETURN 
    nodeType,
    CASE nodeType
        WHEN 'Person' THEN n.name
        WHEN 'Meeting' THEN n.workgroup
        ELSE coalesce(n.title, n.text, '')
    END as nodeName,
    degree as direct_connections,
    count(DISTINCT connected) as reachable_nodes,
    avg(length(path)) as avg_path_length
ORDER BY degree DESC
LIMIT 10;

// 2. Degree Distribution
MATCH (n)
OPTIONAL MATCH (n)-[r]-()
WITH labels(n)[0] as nodeType,
     count(DISTINCT r) as degree
RETURN 
    nodeType,
    degree as connectivity,
    count(*) as node_count
ORDER BY nodeType, degree;

// 3. Clustering Analysis
MATCH (n)-[r1]-(neighbor)
WITH n, 
     collect(DISTINCT neighbor) as neighbors,
     count(DISTINCT neighbor) as degree
WHERE degree > 1
MATCH (n1)-[r2]-(n2)
WHERE n1 IN neighbors 
AND n2 IN neighbors
AND id(n1) < id(n2)
RETURN 
    labels(n)[0] as nodeType,
    degree as node_degree,
    count(*) as neighbor_connections,
    (2.0 * count(*)) / (degree * (degree - 1)) as clustering_coefficient
ORDER BY clustering_coefficient DESC;
```

## Visualization Recommendations

1. **Node Degree Visualization**
```cypher
// Data for degree-based visualization
MATCH (n)
OPTIONAL MATCH (n)-[r]-()
WITH n,
     labels(n)[0] as nodeType,
     count(DISTINCT r) as degree
RETURN 
    nodeType,
    CASE nodeType
        WHEN 'Person' THEN n.name
        WHEN 'Meeting' THEN n.workgroup + ' (' + n.date + ')'
        ELSE coalesce(n.title, n.text, '')
    END as label,
    degree as size
ORDER BY degree DESC;
```
**Visualization Tips:**
- Use node size to represent degree
- Color nodes by type (Person, Meeting, etc.)
- Add tooltips showing exact degree values
- Consider force-directed layout

2. **Path Length Visualization**
```cypher
// Data for path visualization
MATCH path = (start)-[*1..3]-(end)
WHERE labels(start)[0] = 'Person'
AND labels(end)[0] = 'Person'
AND start <> end
RETURN 
    start.name as source,
    end.name as target,
    length(path) as distance,
    [node in nodes(path) | labels(node)[0]] as node_types
ORDER BY distance
LIMIT 100;
```
**Visualization Tips:**
- Use edge length to show path distance
- Color edges by path length
- Show intermediate nodes
- Consider hierarchical layout

3. **Clustering Visualization**
```cypher
// Data for cluster visualization
MATCH (n)-[r1]-(neighbor)
WITH n, 
     collect(DISTINCT neighbor) as neighbors,
     count(DISTINCT neighbor) as degree
WHERE degree > 1
MATCH (n1)-[r2]-(n2)
WHERE n1 IN neighbors 
AND n2 IN neighbors
AND id(n1) < id(n2)
RETURN 
    labels(n)[0] as group,
    n.name as node,
    count(*) as cluster_size,
    collect(DISTINCT n1.name + '-' + n2.name) as connections
ORDER BY cluster_size DESC;
```
**Visualization Tips:**
- Group nodes by clustering coefficient
- Use different colors for clusters
- Show connection density
- Consider circular layout for clusters

### Recommended Visualization Tools:

1. **Neo4j Bloom**
   - Built-in visualization
   - Interactive exploration
   - Custom styling rules
   - Real-time updates

2. **Graph Data Visualization Tools**
   - D3.js for custom web visualizations
   - Gephi for detailed analysis
   - Graphistry for large-scale graphs
   - Cytoscape for biological-style networks

3. **Best Practices**
   - Limit node count for clarity
   - Use consistent color schemes
   - Add interactive filters
   - Include legend/key
   - Enable zoom/pan
   - Show relationship labels on hover

### Visualization Use Cases:

1. **Executive Dashboards**
   - High-level metrics
   - Key player identification
   - Trend visualization

2. **Analysis Views**
   - Detailed connections
   - Path analysis
   - Cluster identification

3. **Operational Views**
   - Real-time updates
   - Action item tracking
   - Meeting connections


