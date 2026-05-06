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
    print("Reading IT Manuals...")

    # 2. Load all Markdown files from the 'docs' folder
    loader = DirectoryLoader('./docs', glob="**/*.md", loader_cls=TextLoader, loader_kwargs={'encoding': 'utf-8'})
    documents = loader.load()
    
    if not documents:
        print("No files found! Make sure you have .md files in the docs folder.")
        return

    print(f"Success: Loaded {len(documents)} document(s).")

    # 3. Split the manuals into chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    raw_chunks = text_splitter.split_documents(documents)
    
    # Filter out any empty chunks
    chunks = [chunk for chunk in raw_chunks if chunk.page_content.strip()]
    
    print(f"Success: Split documents into {len(chunks)} chunks.")

    # 4. Initialize the Google Text Embedding Model
    embeddings = GoogleGenerativeAIEmbeddings(model="gemini-embedding-2-preview")

    # 5. Initialize the database connection
    print("Connecting to local ChromaDB database...")
    vectorstore = Chroma(persist_directory="./chroma_db", embedding_function=embeddings)
    
    # 6. Separate chunks into batches, Loop through batches and translate
    batch_size = 90  
    
    for i in range(0, len(chunks), batch_size):
        batch = chunks[i:i + batch_size]
        print(f"Translating batch {i//batch_size + 1} of {(len(chunks)//batch_size) + 1}...")
        
        try:
            # Attempt to process the whole batch at once
            vectorstore.add_documents(batch)
            
        except IndexError:
            # If Google drops a chunk, translate them 1-by-1
            print("API rejected a chunk! Isolating the blocked text...")
            
            for single_chunk in batch:
                try:
                    vectorstore.add_documents([single_chunk])
                except IndexError:
                    # Skip the blocked chunk and print a preview to show what was flagged
                    snippet = single_chunk.page_content.replace("\n", " ")[:60]
                    print(f"Blocked & Skipped: '{snippet}...'")
        
        # If there are still more chunks to process, pause the script to stay under limit
        if i + batch_size < len(chunks):
            print("Pausing for 60 seconds to limit requests per minute")
            time.sleep(60)
            
    print("The local ChromaDB vector database is ready.\n")

if __name__ == "__main__":
    build_database()