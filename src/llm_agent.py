
import os
import logging
from langchain_community.graphs import Neo4jGraph
from langchain.chains import GraphCypherQAChain
from langchain_openai import ChatOpenAI

# Configure enterprise logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class GraphRAGAgent:
    """
    Orchestrates the Retrieval-Augmented Generation (RAG) pipeline 
    using LangChain, OpenAI, and Neo4j.
    """
    
    def __init__(self, temperature: float = 0.0):
        """Initialize the Graph Connection and the LLM."""
        try:
            # 1. Connect to the Knowledge Graph
            self.graph = Neo4jGraph(
                url=os.getenv("NEO4J_URI"),
                username=os.getenv("NEO4J_USER"),
                password=os.getenv("NEO4J_PASSWORD")
            )
            
            # 2. Initialize the LLM (Temperature 0 for deterministic factual answers)
            self.llm = ChatOpenAI(
                model="gpt-4-turbo-preview", 
                temperature=temperature,
                api_key=os.getenv("OPENAI_API_KEY")
            )
            
            # 3. Create the LangChain Cypher QA Chain
            self.chain = GraphCypherQAChain.from_llm(
                llm=self.llm, 
                graph=self.graph, 
                verbose=True,
                return_direct=False # Set to True if you only want the raw graph data
            )
            logger.info("GraphRAG Agent successfully initialized.")
            
        except Exception as e:
            logger.error(f"Failed to initialize GraphRAG Agent: {str(e)}")
            raise e

    def query(self, user_question: str) -> str:
        """
        Takes a natural language question, queries the graph, and returns the answer.
        """
        logger.info(f"Processing query: {user_question}")
        try:
            response = self.chain.invoke({"query": user_question})
            return response['result']
        except Exception as e:
            logger.error(f"Error during graph traversal: {str(e)}")
            return "I'm sorry, I could not retrieve the factual data for that query."

# --- Example Usage ---
if __name__ == "__main__":
    # agent = GraphRAGAgent()
    # answer = agent.query("Who are the board members of the acquired startup?")
    # print(answer)
    pass