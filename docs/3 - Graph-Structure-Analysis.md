## Graph Structure Analysis

### 1. Node Label Analysis
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

### 2. Relationship Analysis
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

### 3. Graph Schema
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