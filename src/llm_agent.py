import sys
import subprocess
import os
import logging

# Configure enterprise logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# --- INSTALL THE DEDICATED NEO4J-LANGCHAIN PACKAGE ---
logger.info("Verifying enterprise dependencies...")
subprocess.check_call([sys.executable, "-m", "pip", "install", "-q", "langchain", "langchain-neo4j", "langchain-groq"])

# --- MODERN IMPORTS ---
# We use the dedicated Neo4j package instead of generic LangChain community
from langchain_neo4j import Neo4jGraph, GraphCypherQAChain
from langchain_groq import ChatGroq

if __name__ == "__main__":
    # --- 1. Graph & AI Credentials ---
    NEO4J_URI = "neo4j+s://d5eac149.databases.neo4j.io"
    NEO4J_USER = "d5eac149"
    NEO4J_PASSWORD = "UH_MvD8mVLG6WW5gFK4KZvhXkLCqxtjF_MNo2t2mxzs"
    NEO4J_DATABASE = "d5eac149"  # The exact database name
    
    # Your Groq Key
    GROQ_API_KEY = "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" 

    try:
        # --- 2. Connect to the Knowledge Graph ---
        logger.info("Connecting to Neo4j...")
        graph = Neo4jGraph(
            url=NEO4J_URI,
            username=NEO4J_USER,
            password=NEO4J_PASSWORD,
            database=NEO4J_DATABASE
        )
        graph.refresh_schema() 
        logger.info("Graph schema loaded successfully.")

        # --- 3. Initialize Open Source LLM (Llama-3.1 via Groq) ---
        logger.info("Initializing Llama-3.1 LLM...")
        llm = ChatGroq(
            groq_api_key=GROQ_API_KEY,
            model_name="llama-3.1-8b-instant", # The newest active model!
            temperature=0 # Zero hallucinations
        )

        # --- 4. Create the GraphRAG Chain ---
        chain = GraphCypherQAChain.from_llm(
            llm=llm, 
            graph=graph, 
            verbose=True, # Watch Llama write Cypher code in the terminal!
            allow_dangerous_requests=True # Bypass LangChain security block for testing
        )

        # --- 5. Talk to the Data! ---
        print("\n" + "="*50)
        # Schema Hint: We tell the AI exactly where to look!
        question = """
        Use exactly this Cypher query to get the data: 
        MATCH (d:Document) RETURN d.content
        
        Based on the text returned, what kind of architects are Databricks and Visa hiring?
        """
        logger.info(f"User Question: {question}")
        
        response = chain.invoke({"query": question})
        
        print("="*50)
        print(f"🤖 AI FINAL ANSWER: {response['result']}")
        print("="*50 + "\n")

    except Exception as e:
        logger.error(f"Execution failed: {str(e)}")