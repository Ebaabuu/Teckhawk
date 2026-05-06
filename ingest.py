import os
import time  
from dotenv import load_dotenv
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma

# Load environment variables (API keys)
load_dotenv()

def build_database():
    """
    Ingests local Markdown documentation, chunks the text, and generates mathematical 
    embeddings using Google's Gemini API. The resulting vectors are stored locally 
    in a persistent ChromaDB instance for retrieval-augmented generation (RAG).
    """
    print("Initializing Knowledge Base Ingestion...")

    # ==========================================
    # 1. Document Loading
    # ==========================================
    # Crawl the 'docs' directory for all markdown files. 
    # Enforce UTF-8 encoding to prevent Windows/Mac character map clashes.
    loader = DirectoryLoader('./docs', glob="**/*.md", loader_cls=TextLoader, loader_kwargs={'encoding': 'utf-8'})
    documents = loader.load()
    
    if not documents:
        print("No files found! Make sure you have .md files in the docs folder.")
        return

    print(f"Success: Loaded {len(documents)} document(s).")

    # ==========================================
    # 2. Text Splitting & Chunking
    # ==========================================
    # Break large manuals into smaller semantic chunks for the vector database.
    # chunk_overlap ensures that sentences at the edge of a chunk don't lose context.
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    raw_chunks = text_splitter.split_documents(documents)
    
    # Filter out any empty chunks
    chunks = [chunk for chunk in raw_chunks if chunk.page_content.strip()]
    print(f"Success: Split documents into {len(chunks)} chunks.")

    # ==========================================
    # 3. Vector Database Initialization
    # ==========================================
    # Initialize the Google Text Embedding Model
    embeddings = GoogleGenerativeAIEmbeddings(model="gemini-embedding-2-preview")
    print("Connecting to local ChromaDB database...")
    
    # Instantiate the database connector pointing to the local hard drive
    vectorstore = Chroma(persist_directory="./chroma_db", embedding_function=embeddings)
    
    # ==========================================
    # 4. Batch Processing & Rate Limit Management
    # ==========================================
    # The free tier of the Google Gemini API has strict Requests-Per-Minute (RPM) limits.
    # We process chunks in batches to optimize network calls, then pause to respect the rate wall.
    batch_size = 90  
    
    for i in range(0, len(chunks), batch_size):
        batch = chunks[i:i + batch_size]
        print(f"Translating batch {i//batch_size + 1} of {(len(chunks)//batch_size) + 1}...")
        
        try:
            # Attempt to process the whole batch at once
            vectorstore.add_documents(batch)
            
        except IndexError:
            # Google's API will throw an IndexError if its safety filter flags a specific chunk
            # (e.g., mistaking IT security policies for hacking instructions).
            # This alternate method drops to 1-by-1 processing to isolate and skip the offending chunk.
            print("API rejected a chunk! Isolating the blocked text...")
            
            for single_chunk in batch:
                try:
                    vectorstore.add_documents([single_chunk])
                except IndexError:
                    # Skip the blocked chunk and print a preview to show what was flagged
                    snippet = single_chunk.page_content.replace("\n", " ")[:60]
                    print(f"Blocked by API & Skipped: '{snippet}...'")
        
        # If there are more batches remaining, enforce a cooldown period to reset the RPM limit
        if i + batch_size < len(chunks):
            print("Pausing for 60 seconds to limit requests per minute")
            time.sleep(60)
            
    print("The local ChromaDB vector database is ready.\n")

if __name__ == "__main__":
    build_database()