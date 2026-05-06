# TechHawk IT Help Desk

A local Retrieval-Augmented Generation (RAG) prototype built specifically for the University of Kansas Edwards Campus IT department. 

TechHawk serves as a highly accurate, conversational IT assistant. It securely searches a localized vector database of official KU Edwards manuals to answer student and faculty questions without hallucinating, providing exact troubleshooting steps and policy guidelines.

---

## Key Features

* **Multi-Model Switchboard:** Seamlessly toggle between Google Gemini 2.5 Flash, Ollama, and OpenAI ChatGPT (GPT-5.4 Mini) via the sidebar UI to compare generation speed and answer accuracy in real-time.
* **Persistent Chat Sessions:** Chat history is dynamically saved. Users can pin, rename, share, and delete previous conversations.
* **Local Vector Database:** Built using LangChain and ChromaDB, the application stores data embeddings locally on the hard drive, ensuring data privacy and drastically reducing cloud compute costs.
* **Hybrid Retrieval:** Utilizes Maximal Marginal Relevance (MMR) search logic to ensure the AI receives diverse, highly accurate context from the IT manuals rather than redundant paragraphs.
* **File Context Analysis:** Supports multi-file uploads directly in the chat interface, allowing the AI to read user-provided documents alongside the official IT manuals.

---

## Project Architecture & The RAG Pipeline

Understanding how TechHawk separates retrieving data from generating answers is critical for future development. The system uses two completely different types of AI models that do two distinct jobs.

### 1. The Embedder (The Librarian)
We use Google's gemini-embedding-2-preview exclusively to translate plain English into mathematical vectors. 
* **Data Ingestion:** When ingest.py runs, the embedder translates the manuals into math and stores them locally.
* **Querying:** When a user asks a question, the embedder translates the question into math so ChromaDB can mathematically find the closest matching paragraphs using Cosine Similarity.
* **Vector DB vs Knowledge Graph:** We use a Vector Database (ChromaDB), which maps semantic proximity (how close text means the same thing mathematically). It is not a Knowledge Graph, which maps explicit, rigid logical relationships. All data is stored 100% locally on your machine.

### 2. The Language Model (The Brain/Speaker)
This is Gemini 2.5 Flash, ChatGPT, or Ollama. 
* The Language Model never sees the mathematical vectors. 
* Once ChromaDB finds the relevant information, it strips the math away and hands the plain English text to the Language Model.
* Because the AI only reads English, you can swap between Google, OpenAI, or local models seamlessly using the switchboard without having to rebuild the database.

---

## Prerequisites & Initial Setup

Before you begin, ensure you have the following installed:
* Python 3.11 or higher
* Git

Crucial Setup Note for New Computers: If installing Python on a brand-new Windows PC, you MUST check the box that says "Add python.exe to PATH" at the bottom of the installer window. If you miss this, terminal commands like python and pip will return a "not recognized" error.

### 1. Clone the Repository
git clone https://github.com/your-username/techhawk-capstone.git
cd techhawk-capstone

### 2. Install Dependencies
pip install -r requirements.txt

### 3. Configure Environment Variables & Security
You must provide your own API keys. Create a file named .env in the root directory and add:

GOOGLE_API_KEY=your_google_api_key_here
OPENAI_API_KEY=your_openai_api_key_here

---

## Building the Knowledge Base

1. Place your Markdown (.md) formatted IT manuals into the docs/ directory.
2. Run the ingestion script:

python ingest.py

## Running the Application

Launch the TechHawk Streamlit interface:

streamlit run app.py

---

### How to Reduce Token Consumption
If your app crashes from payload limits during testing, implement these optimizations:
1. **Shrink Chunk Sizes:** In ingest.py, reduce the RecursiveCharacterTextSplitter from 1000 to 500 characters.
2. **Lower Context Window:** In brain.py, change the retriever setting from k=3 to k=2.
3. **Stop the Chat Snowball:** Implement a sliding window memory so LangChain only remembers the last 2 interactions instead of appending the entire chat history indefinitely.
