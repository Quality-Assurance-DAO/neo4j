from neo4j import GraphDatabase
import logging
from typing import Optional, Dict, Any
import os
from dotenv import load_dotenv
import json

class AuraConnection:
    def __init__(self):
        """Initialize the Neo4j Aura connection handler"""
        # Debug: Read .env file directly
        try:
            with open('.env', 'r') as f:
                print("Raw .env contents:")
                print(repr(f.read()))  # Using repr() to show hidden characters
        except Exception as e:
            print(f"Error reading .env: {e}")
        
        load_dotenv()
        
        # Debug: Check if .env file is being found
        print(f"Current working directory: {os.getcwd()}")
        print(f"Does .env exist?: {os.path.exists('.env')}")
        
        # Connection details should be stored in environment variables
        self.uri = os.getenv('NEO4J_URI')  # Aura connection URI
        self.username = os.getenv('NEO4J_USERNAME')  # Usually 'neo4j'
        self.password = os.getenv('NEO4J_PASSWORD')  # Your Aura instance password
        
        # Debug: Print all environment variables
        print("Environment variables:")
        print(f"NEO4J_URI: {os.getenv('NEO4J_URI')}")
        print(f"NEO4J_USERNAME: {os.getenv('NEO4J_USERNAME')}")
        
        # Initialize logger
        self.logger = logging.getLogger(__name__)
        
        # Initialize driver as None
        self.driver: Optional[GraphDatabase.driver] = None

    def connect(self) -> bool:
        """
        Establish connection to Neo4j Aura instance
        Returns: bool indicating if connection was successful
        """
        try:
            # Debug prints
            print(f"URI type: {type(self.uri)}")
            print(f"URI value: {self.uri}")
            print(f"Username: {self.username}")
            
            # Create the driver instance
            self.driver = GraphDatabase.driver(
                self.uri,
                auth=(self.username, self.password),
                max_connection_lifetime=3600,
                max_connection_pool_size=50,
                connection_acquisition_timeout=60
            )
            
            # Verify connectivity
            self.driver.verify_connectivity()
            
            self.logger.info("Successfully connected to Neo4j Aura instance")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to connect to Neo4j Aura: {str(e)}")
            return False

    def close(self):
        """Close the Neo4j connection"""
        if self.driver:
            self.driver.close()
            self.logger.info("Neo4j Aura connection closed")

    def test_connection(self) -> bool:
        """
        Test the connection by running a simple query
        Returns: bool indicating if test was successful
        """
        try:
            with self.driver.session() as session:
                result = session.run("RETURN 1 AS test")
                return result.single()["test"] == 1
        except Exception as e:
            self.logger.error(f"Connection test failed: {str(e)}")
            return False

    def execute_query(self, query: str, parameters: dict = None) -> list:
        """
        Execute a Cypher query and return the results
        
        Args:
            query: Cypher query string
            parameters: Optional dictionary of query parameters
            
        Returns:
            List of records from the query
        """
        try:
            with self.driver.session() as session:
                result = session.run(query, parameters or {})
                return [record.data() for record in result]
        except Exception as e:
            self.logger.error(f"Query execution failed: {str(e)}")
            raise

    def import_json_data(self, json_file_path: str) -> bool:
        """
        Import SingularityNET meeting data from JSON file into Neo4j
        """
        try:
            with open(json_file_path, 'r') as file:
                data = json.load(file)
            
            with self.driver.session() as session:
                # First, clear existing data
                session.run("MATCH (n) DETACH DELETE n")
                
                for meeting_id, meetings in data.items():
                    for meeting in meetings:
                        # Create Meeting node
                        meeting_query = """
                        CREATE (m:Meeting {
                            id: $meeting_id,
                            workgroup: $workgroup,
                            workgroup_id: $workgroup_id,
                            name: $name,
                            date: $date,
                            host: $host,
                            documenter: $documenter,
                            purpose: $purpose
                        })
                        """
                        meeting_info = meeting['meetingInfo']
                        session.run(meeting_query, {
                            'meeting_id': meeting_id,
                            'workgroup': meeting['workgroup'],
                            'workgroup_id': meeting['workgroup_id'],
                            'name': meeting_info['name'],
                            'date': meeting_info['date'],
                            'host': meeting_info['host'],
                            'documenter': meeting_info['documenter'],
                            'purpose': meeting_info['purpose']
                        })
                        
                        # Create Participant nodes and relationships
                        participants_query = """
                        MATCH (m:Meeting {id: $meeting_id})
                        WITH m
                        UNWIND $participants AS participant
                        MERGE (p:Person {name: participant})
                        CREATE (p)-[:ATTENDED]->(m)
                        """
                        participants = [p.strip() for p in meeting_info['peoplePresent'].split(',')]
                        session.run(participants_query, {
                            'meeting_id': meeting_id,
                            'participants': participants
                        })
                        
                        # Create Document nodes and relationships
                        docs_query = """
                        MATCH (m:Meeting {id: $meeting_id})
                        WITH m
                        UNWIND $docs AS doc
                        CREATE (d:Document {
                            title: doc.title,
                            link: doc.link
                        })
                        CREATE (m)-[:HAS_DOCUMENT]->(d)
                        """
                        session.run(docs_query, {
                            'meeting_id': meeting_id,
                            'docs': meeting_info['workingDocs']
                        })
                        
                        # Create Agenda Items and their components
                        agenda_query = """
                        MATCH (m:Meeting {id: $meeting_id})
                        WITH m
                        UNWIND $agenda_items AS item
                        CREATE (a:AgendaItem {
                            status: item.status,
                            narrative: item.narrative
                        })
                        CREATE (m)-[:HAS_AGENDA_ITEM]->(a)
                        
                        // Create Discussion Points
                        WITH a, item
                        UNWIND item.discussionPoints AS point
                        CREATE (d:DiscussionPoint {text: point})
                        CREATE (a)-[:INCLUDES_DISCUSSION]->(d)
                        
                        // Create Decision Items
                        WITH a, item
                        UNWIND item.decisionItems AS decision
                        CREATE (dec:Decision {
                            decision: decision.decision,
                            rationale: decision.rationale,
                            opposing: decision.opposing,
                            effect: decision.effect
                        })
                        CREATE (a)-[:MADE_DECISION]->(dec)
                        """
                        
                        for agenda_item in meeting['agendaItems']:
                            session.run(agenda_query, {
                                'meeting_id': meeting_id,
                                'agenda_items': [{
                                    'status': agenda_item.get('status', ''),
                                    'narrative': agenda_item.get('narrative', ''),
                                    'discussionPoints': agenda_item.get('discussionPoints', []),
                                    'decisionItems': agenda_item.get('decisionItems', [])
                                }]
                            })
                        
                        # Create Action Items with relationships
                        actions_query = """
                        MATCH (m:Meeting {id: $meeting_id})
                        WITH m
                        UNWIND $actions AS action
                        CREATE (a:ActionItem {
                            text: action.text,
                            status: action.status,
                            dueDate: action.dueDate
                        })
                        CREATE (m)-[:HAS_ACTION]->(a)
                        WITH a, action
                        MATCH (p:Person {name: action.assignee})
                        CREATE (a)-[:ASSIGNED_TO]->(p)
                        """
                        
                        # Flatten action items from all agenda items
                        all_actions = []
                        for agenda_item in meeting['agendaItems']:
                            all_actions.extend([
                                action for action in agenda_item.get('actionItems', [])
                                if 'assignee' in action
                            ])
                        
                        if all_actions:
                            session.run(actions_query, {
                                'meeting_id': meeting_id,
                                'actions': all_actions
                            })
                
                self.logger.info(f"Successfully imported meeting data from {json_file_path}")
                return True
                
        except Exception as e:
            self.logger.error(f"Failed to import JSON data: {str(e)}")
            return False

def main():
    # Set up logging
    logging.basicConfig(level=logging.INFO)
    
    # Create a .env file with your Aura credentials:
    """
    NEO4J_URI=neo4j+s://xxxxxxxx.databases.neo4j.io
    NEO4J_USERNAME=neo4j
    NEO4J_PASSWORD=your-password
    """
    
    # Initialize connection
    aura = AuraConnection()
    
    try:
        # Connect to Aura
        if aura.connect():
            # Test the connection
            if aura.test_connection():
                print("Successfully connected to Neo4j Aura!")
                
                # Example query
                result = aura.execute_query(
                    "MATCH (n) RETURN count(n) as node_count"
                )
                print(f"Number of nodes in database: {result[0]['node_count']}")
                
                # Import JSON data with explicit path
                json_path = os.path.join(os.getcwd(), 'snet-data.json')
                if aura.import_json_data(json_path):
                    print("Successfully imported data from JSON!")
                else:
                    print("Failed to import data from JSON!")
            else:
                print("Connection test failed!")
        else:
            print("Failed to connect to Neo4j Aura!")
            
    finally:
        # Always close the connection
        aura.close()

if __name__ == "__main__":
    main()