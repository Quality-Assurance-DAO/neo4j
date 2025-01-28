from neo4j import GraphDatabase
import logging
from typing import Optional
import os
from dotenv import load_dotenv

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
            else:
                print("Connection test failed!")
        else:
            print("Failed to connect to Neo4j Aura!")
            
    finally:
        # Always close the connection
        aura.close()

if __name__ == "__main__":
    main()