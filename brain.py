import os
import streamlit as st
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder # <-- NEW IMPORT

load_dotenv()

def load_rag_chain():
    try:
        if not os.getenv("GOOGLE_API_KEY"):
            st.error("API Key missing! Please check your .env file.")
            return None
        
        embeddings = GoogleGenerativeAIEmbeddings(model="gemini-embedding-2-preview")
        vectorstore = Chroma(persist_directory="./chroma_db", embedding_function=embeddings)
        # retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
        # Configure the retriever to use MMR
        retriever = vectorstore.as_retriever(
            search_type="mmr",
            search_kwargs={
                "k": 3,              # Number of chunks to eventually send to the AI
                "fetch_k": 10,       # Number of chunks to initially fetch to find diversity
                "lambda_mult": 0.5   # The balance: 1.0 is pure relevance, 0.0 is pure diversity
        }
)
        llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.3)
        
        system_prompt = (
            "You are the official TechHawk IT Help Desk Assistant for the Edwards Campus. "
            "Use the following pieces of retrieved context to answer the question. "
            "Use a friendly, helpful, and encouraging demeanor when talking to the user."
            "If the question is unclear, ask probing questions to guide the user.\n\n"
            "You must always end your response by providing the Edwards IT phone number: 913-897-8652."
            "Context from Manuals:\n{context}\n\n"
            "Context from User Uploaded Files:\n{file_context}"
        )
        
        # --- NEW: Added MessagesPlaceholder for chat_history ---
        prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            MessagesPlaceholder(variable_name="chat_history"), 
            ("human", "{input}"),
        ])
        
        # --- NEW: Adjusted the chain to handle dictionary inputs ---
        return (
            {
                "context": (lambda x: x["input"]) | retriever | (lambda docs: "\n\n".join(d.page_content for d in docs)), 
                "file_context": lambda x: x.get("file_context", ""), 
                "chat_history": lambda x: x.get("chat_history", []),
                "input": lambda x: x["input"]
            } 
            | prompt | llm | StrOutputParser()
        )
    except Exception as e:
        st.error(f"Error loading AI: {e}")
        return None