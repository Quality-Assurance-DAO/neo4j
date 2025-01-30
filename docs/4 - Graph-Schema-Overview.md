## Graph Schema Overview
```cypher
// Schema-level view
MATCH (a)-[r]->(b)
WITH DISTINCT
    labels(a)[0] as Source_Type,
    type(r) as Relationship,
    labels(b)[0] as Target_Type
RETURN 
    Source_Type + ' -[' + Relationship + ']-> ' + Target_Type as Graph_Structure
ORDER BY Source_Type, Relationship;
```

This query shows the high-level structure of the graph, displaying all node types and how they are connected through relationships.