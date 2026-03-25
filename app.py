import streamlit as st
import os
import time
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

# Securely load the API key
load_dotenv()

# Set up the Streamlit Web Interface
st.set_page_config(page_title="TechHawk IT Assistant", page_icon="🦅")
st.title("TechHawk IT Help Desk")
st.markdown("Welcome to the secure Edwards Campus IT Assistant.")

# Connect the AI and Database
@st.cache_resource
def load_ai_components():
    # 1. Concept Translator
    embeddings = GoogleGenerativeAIEmbeddings(model="gemini-embedding-2-preview")
    
    # 2. Connect to local database
    vectorstore = Chroma(persist_directory="./chroma_db", embedding_function=embeddings)
    retriever = vectorstore.as_retriever(search_kwargs={"k": 3}) 
    
    # 3. Set up the Brain
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.3)
    
    # 4. Give the AI its strict instructions
    system_prompt = (
        "You are the official TechHawk IT Help Desk Assistant for the Edwards Campus. "
        "Use the following pieces of retrieved context to answer the question. "
        "If the answer is not in the context, say exactly: 'I cannot answer that based on the official IT manuals.' "
        "Do not guess or make up information. Keep the answer concise and helpful.\n\n"
        "Context:\n{context}"
    )
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", "{input}"),
    ])
    
    # Helper function to add newlines to the retrieved documents
    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)
    
    # 5. The Modern LCEL Pipeline (Bypasses the broken 'chains' module)
    rag_chain = (
        {"context": retriever | format_docs, "input": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    
    return rag_chain

# Initialize the pipeline
rag_chain = load_ai_components()

# Initialize chat history in session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display past chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Initialize the cooldown timer in session state
if "last_msg_time" not in st.session_state:
    st.session_state.last_msg_time = 0

# Handle new user input
if user_query := st.chat_input("Ask an IT question..."):
    
    # DOS Defense: Cooldown timer and Error Catching
    current_time = time.time()
    if current_time - st.session_state.last_msg_time < 5:
        st.warning("Please wait a few seconds before sending another message.")
    else:
        # Update the timer to the current time
        st.session_state.last_msg_time = current_time
        
        # Show user message on screen
        st.chat_message("user").markdown(user_query)
        st.session_state.messages.append({"role": "user", "content": user_query})
        
        # Show a loading spinner while the AI searches
        with st.spinner("Searching official IT Manuals..."):
            try:
                # Send the query through the LangChain pipeline
                ai_answer = rag_chain.invoke(user_query)
                
            except Exception as e:
                # If Google crashes or rate-limits us, show an error instead of crashing the app
                ai_answer = "The system is currently receiving too many requests. Please try again in a minute."
                print(f"API Error encountered: {e}") # Logs the real error in your terminal
        
        # Show AI response on screen
        with st.chat_message("assistant"):
            st.markdown(ai_answer)
        st.session_state.messages.append({"role": "assistant", "content": ai_answer})