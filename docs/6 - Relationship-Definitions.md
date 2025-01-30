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