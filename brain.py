import os
import streamlit as st
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama
from langchain_chroma import Chroma
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

load_dotenv()

def load_rag_chain(selected_model="Gemini 2.5 Flash"):
    """
    Initializes and returns the Retrieval-Augmented Generation (RAG) pipeline.
    Handles embedding, vector search, prompt injection, and LLM generation.
    
    Args:
        selected_model (str): The generative model selected by the user in the UI.
        
    Returns:
        Runnable: A compiled LangChain pipeline, or None if initialization fails.
    """
    try:
        # ==========================================
        # 1. API Security Validation
        # ==========================================
        # Fail early if keys are missing to prevent cryptic LangChain crash traces
        if not os.getenv("GOOGLE_API_KEY"):
            st.error("Google API Key missing! Please check your .env file.")
            return None
        
        if selected_model == "ChatGPT (GPT-5.4 Mini)" and not os.getenv("OPENAI_API_KEY"):
            st.error("OpenAI API Key missing! Please check your .env file.")
            return None
        
        # ==========================================
        # 2. Vector Store & Retriever Initialization
        # ==========================================
        # MUST use Gemini Embeddings regardless of selected LLM, 
        # as the ChromaDB database was compiled using this specific mathematical model.
        embeddings = GoogleGenerativeAIEmbeddings(model="gemini-embedding-2-preview")
        vectorstore = Chroma(persist_directory="./chroma_db", embedding_function=embeddings)
        
        # Configure Maximal Marginal Relevance (MMR) search logic.
        # fetch_k = initial broad pool, k = final filtered chunks sent to LLM.
        retriever = vectorstore.as_retriever(
            search_type="mmr",
            search_kwargs={"k": 3, "fetch_k": 10, "lambda_mult": 0.5}
        )
        
        # ==========================================
        # 3. LLM Switchboard
        # ==========================================
        # Instantiate the specific Generative Model requested by the Streamlit frontend.
        # Temperature set to 0.3 to favor factual accuracy over creative hallucination.
        if selected_model == "Gemini 2.5 Flash":
            llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.3)
        elif selected_model == "ChatGPT (GPT-5.4 Mini)":
            llm = ChatOpenAI(model="gpt-5.4-mini", temperature=0.3)
        elif selected_model == "Ollama (Local)":
            llm = ChatOllama(model="llama3.2", temperature=0.3)
        else:
            raise ValueError(f"Unknown model: {selected_model}")
            
        # ==========================================
        # 4. Prompt Engineering
        # ==========================================
        system_prompt = (
            "You are the official TechHawk IT Help Desk Assistant for the Edwards Campus. "
            "Use the following pieces of retrieved context to answer the question. "
            "Use a friendly, helpful, and encouraging demeanor when talking to the user."
            "If the question is unclear, ask probing questions to guide the user.\n\n"
            "You must always end your response by providing the Edwards IT phone number: 913-897-8652."
            "Context from Manuals:\n{context}\n\n"
            "Context from User Uploaded Files:\n{file_context}"
        )
        
        # Construct the final prompt array handling system instructions, memory, and current input
        prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            MessagesPlaceholder(variable_name="chat_history"), 
            ("human", "{input}"),
        ])
        
        # ==========================================
        # 5. LCEL Pipeline Construction
        # ==========================================
        # Dictionary dynamically maps the incoming request payload to the prompt variables.
        # It executes the retriever using the "input" string, formats the resulting docs,
        # and passes everything through the Prompt -> LLM -> String Parser.
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
        # Catch network timeouts or model instantiation failures
        st.error(f"Error loading AI: {e}")
        return None