
import os
from neo4j import GraphDatabase
import logging
from dotenv import load_dotenv

# Load environment variables from the .env file we created
load_dotenv()

# Configure basic logging for enterprise observability
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class KnowledgeGraphBuilder:
    """
    Enterprise Knowledge Graph Builder for Neo4j.
    Handles secure connections, schema creation, and data ingestion.
    """
    
    def __init__(self, uri: str, user: str, password: str):
        """Initialize the Neo4j driver connection."""
        try:
            self.driver = GraphDatabase.driver(uri, auth=(user, password))
            logger.info("Successfully connected to Neo4j Enterprise Graph.")
        except Exception as e:
            logger.error(f"Failed to connect to Neo4j: {str(e)}")
            raise e

    def close(self):
        """Close the database connection securely."""
        if self.driver:
            self.driver.close()
            logger.info("Neo4j connection closed.")

    def create_constraints(self):
        """
        Create unique constraints on the graph to prevent data duplication.
        This is a critical step for deterministic GraphRAG.
        """
        with self.driver.session() as session:
            # We run these individually as best practice for Neo4j Python Driver
            session.run("CREATE CONSTRAINT unique_document IF NOT EXISTS FOR (d:Document) REQUIRE d.id IS UNIQUE;")
            session.run("CREATE CONSTRAINT unique_entity IF NOT EXISTS FOR (e:Entity) REQUIRE e.name IS UNIQUE;")
            logger.info("Graph constraints verified and applied.")

    def ingest_document_nodes(self, document_id: str, content: str):
        """
        Example method to ingest unstructured text as a Document Node.
        """
        query = """
        MERGE (d:Document {id: $doc_id})
        SET d.content = $content, d.processed = true
        RETURN d
        """
        with self.driver.session() as session:
            session.run(query, doc_id=document_id, content=content)
            logger.info(f"Ingested Document Node: {document_id}")

# --- Execute the Architecture ---
# --- Execute the Architecture ---
if __name__ == "__main__":
    # Using the EXACT credentials from your new instance
    NEO4J_URI = "neo4j+s://d5eac149.databases.neo4j.io"
    NEO4J_USER = "d5eac149"   # <-- This was the missing puzzle piece!
    NEO4J_PASSWORD = "UH_MvD8mVLG6WW5gFK4KZvhXkLCqxtjF_MNo2t2mxzs"
    
    # 1. Initialize the builder
    kg_builder = KnowledgeGraphBuilder(NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD)
    
    # 2. Create schema constraints
    kg_builder.create_constraints()
    
    # 3. Add a sample document to the Graph
    kg_builder.ingest_document_nodes(
        document_id="DOC_001", 
        content="Databricks and Visa are hiring elite AI Architects."
    )
    
    # 4. Close the connection securely
    kg_builder.close()