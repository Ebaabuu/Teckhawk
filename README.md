# TechHawk IT Help Desk

A local Retrieval-Augmented Generation (RAG) prototype built specifically for the University of Kansas Edwards Campus IT department. 

TechHawk serves as a highly accurate, conversational IT assistant. It securely searches a localized vector database of official KU Edwards manuals to answer student and faculty questions without hallucinating, providing exact troubleshooting steps and policy guidelines.

## Prerequisites & Initial Setup

Before you begin, ensure you have the following installed:
* Python 3.11 or higher
* Git

Crucial Setup Note for New Computers: If installing Python on a brand-new Windows PC, you MUST check the box that says "Add python.exe to PATH" at the bottom of the installer window. If you miss this, terminal commands like python and pip will return a "not recognized" error.

### 1. Clone the Repository
git clone https://github.com/Ebaabuu/Teckhawk.git
cd TechHawk

### 2. Install Dependencies
pip install -r requirements.txt

### 3. Configure Environment Variables & Security
You must provide your own API keys. Create a file named .env in the root directory and add:

GOOGLE_API_KEY=your_google_api_key_here
OPENAI_API_KEY=your_openai_api_key_here

## Building the Knowledge Base

1. Place your Markdown (.md) formatted IT manuals into the docs/ directory.
2. Run the ingestion script:

python ingest.py

## 4. Running the Application

Launch the TechHawk Streamlit interface:

python -m streamlit run app.py
