import os
import streamlit as st
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

# This looks for the .env file and loads the key privately
load_dotenv()

def load_rag_chain():
    try:
        # Check if the key exists before starting
        if not os.getenv("GOOGLE_API_KEY"):
            st.error("API Key missing! Please check your .env file.")
            return None
        
        # 1. Concept Translator
        embeddings = GoogleGenerativeAIEmbeddings(model="gemini-embedding-2-preview")
        
        # 2. Connect to local database
        vectorstore = Chroma(persist_directory="./chroma_db", embedding_function=embeddings)
        retriever = vectorstore.as_retriever(search_kwargs={"k": 3}) 
        
        # 3. Set up the Brain (Using 1.5-flash for stability)
        llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.3)
        
        # 4. Your Strict IT Help Desk Instructions
        system_prompt = (
            "You are the official TechHawk IT Help Desk Assistant for the Edwards Campus. "
            "Use the following pieces of retrieved context to answer the question. "
            "If the answer is not in the context, say exactly: 'I cannot answer that based on the official IT manuals.' "
            "Do not guess or make up information. Keep the answer concise and helpful.\n\n"
            "Context from Manuals:\n{context}\n\n"
            "Context from User Uploaded Files:\n{file_context}"
        )
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            ("human", "{input}"),
        ])
        
        # Create the chain
        return (
            {"context": retriever | (lambda docs: "\n\n".join(d.page_content for d in docs)), 
             "file_context": RunnablePassthrough(), 
             "input": RunnablePassthrough()} 
            | prompt | llm | StrOutputParser()
        )
    except Exception as e:
        st.error(f"Error loading AI: {e}")
        return None