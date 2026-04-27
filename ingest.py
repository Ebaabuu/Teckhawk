import os
import time  
from dotenv import load_dotenv
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma

# 1. Securely load the API key
load_dotenv()

def build_database():
    print("Starting Phase A: Reading IT Manuals...")

    # 2. Load all Markdown files from the 'docs' folder
    loader = DirectoryLoader('./docs', glob="**/*.md", loader_cls=TextLoader, loader_kwargs={'encoding': 'utf-8'})
    documents = loader.load()
    
    if not documents:
        print("No files found! Make sure you have .md files in the docs folder.")
        return

    print(f"Success: Loaded {len(documents)} document(s).")

    # 3. Split the manuals into bite-sized paragraphs
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    raw_chunks = text_splitter.split_documents(documents)
    
    # --- FIX 1: Filter out any empty or whitespace-only chunks ---
    chunks = [chunk for chunk in raw_chunks if chunk.page_content.strip()]
    
    print(f"Success: Split documents into {len(chunks)} chunks.")

    # 4. Initialize the Google Text Embedding Model
    embeddings = GoogleGenerativeAIEmbeddings(model="gemini-embedding-2-preview")

    # 5. Initialize the database connection
    print("Connecting to local Chroma database...")
    vectorstore = Chroma(persist_directory="./chroma_db", embedding_function=embeddings)
    
    # 6. The "Throttle" Loop (With Defensive Fallback)
    batch_size = 90  
    
    for i in range(0, len(chunks), batch_size):
        batch = chunks[i:i + batch_size]
        print(f"Translating batch {i//batch_size + 1} of {(len(chunks)//batch_size) + 1}...")
        
        try:
            # First, attempt to process the whole batch of 90 at once
            vectorstore.add_documents(batch)
            
        except IndexError:
            # --- FIX 2: If Google dropped a chunk, fall back to 1-by-1 ---
            print("API rejected a chunk! Isolating the blocked text...")
            
            for single_chunk in batch:
                try:
                    vectorstore.add_documents([single_chunk])
                except IndexError:
                    # Skip the blocked chunk and print a preview so you know what was flagged
                    snippet = single_chunk.page_content.replace("\n", " ")[:60]
                    print(f"Blocked & Skipped: '{snippet}...'")
        
        # If there are still more chunks to process, pause the script
        if i + batch_size < len(chunks):
            print("Pausing for 60 seconds to limit requests per minute")
            time.sleep(60)
            
    print("Phase A Complete! The local ChromaDB vector store is ready.")

if __name__ == "__main__":
    build_database()