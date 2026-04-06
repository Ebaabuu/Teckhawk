import streamlit as st
import uuid
import os
from sidebar import render_sidebar
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

# 1. Setup
load_dotenv()
st.set_page_config(page_title="TechHawk IT Assistant", layout="wide")

# THE FULL CSS
st.markdown("""
    <style>
    .centered-header { text-align: center; margin-top: -20px; }
    .centered-subheader { text-align: center; color: #666; margin-bottom: 30px; }
    .main .block-container { max-width: 1100px; }

    /* --- HAMBURGER ICON --- */
    [data-testid="stSidebarCollapsedControl"] button svg { display: none !important; }
    [data-testid="stSidebarCollapsedControl"] button::before {
        content: "☰" !important; font-size: 26px !important; color: black !important; font-weight: bold !important;
    }

    /* --- SIDEBAR PILLS & THREE DOTS --- */
    [data-testid="stVerticalBlockBorderWrapper"] > div > div > div[data-testid="stVerticalBlock"] > div { position: relative !important; }
    
    [data-testid="stSidebar"] .stButton > button {
        border-radius: 20px !important; background-color: #e0e0e0 !important; color: black !important;
        height: 40px !important; text-align: left !important; width: 100% !important; padding-left: 15px !important;
    }

    [data-testid="stSidebar"] div[data-testid="stPopover"] {
        position: absolute !important; right: 12px !important; margin-top: -55px !important; 
        width: 30px !important; height: 40px !important; z-index: 99 !important; opacity: 0; pointer-events: none;
    }

    [data-testid="stVerticalBlock"] > div:hover div[data-testid="stPopover"] { opacity: 1 !important; pointer-events: auto !important; }

    [data-testid="stSidebar"] [data-testid="stPopover"] svg { display: none !important; }
    [data-testid="stSidebar"] [data-testid="stPopover"] button div:last-child { display: none !important; }
    [data-testid="stSidebar"] [data-testid="stPopover"] button::before { content: "⋮"; font-size: 22px; color: #444; font-weight: bold; }
    [data-testid="stSidebar"] [data-testid="stPopover"] button { background: transparent !important; border: none !important; box-shadow: none !important; }

    /* --- TOOL MENU LEFT ALIGNMENT --- */
    div[data-testid="stPopoverContent"] { background-color: white !important; border: 1px solid #ddd !important; border-radius: 8px !important; padding: 4px 0px !important; min-width: 135px !important; }
    div[data-testid="stPopoverContent"] button, div[data-testid="stPopoverContent"] button > div { display: flex !important; justify-content: flex-start !important; align-items: center !important; width: 100% !important; }
    div[data-testid="stPopoverContent"] button p { margin: 0 !important; text-align: left !important; width: 100% !important; }

    /* --- CHAT MIDDLE BARRIER --- */
    [data-testid="stChatMessage"]:has([data-testid="stChatMessageUserAvatar"]) { flex-direction: row-reverse !important; }
    </style>
    """, unsafe_allow_html=True)

# 2. AI Logic
@st.cache_resource
def load_ai_components():
    try:
        embeddings = GoogleGenerativeAIEmbeddings(model="gemini-embedding-2-preview")
        vectorstore = Chroma(persist_directory="./chroma_db", embedding_function=embeddings)
        retriever = vectorstore.as_retriever(search_kwargs={"k": 3}) 
        llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.3)
        system_prompt = ("You are the official TechHawk IT Help Desk Assistant. Context:\n{context}")
        prompt = ChatPromptTemplate.from_messages([("system", system_prompt), ("human", "{input}")])
        return ({"context": retriever | (lambda docs: "\n\n".join(d.page_content for d in docs)), "input": RunnablePassthrough()} | prompt | llm | StrOutputParser())
    except: return None

rag_chain = load_ai_components()

# 3. Session State
if "chat_sessions" not in st.session_state: st.session_state.chat_sessions = {}
if "current_chat_id" not in st.session_state: st.session_state.current_chat_id = None

# 4. Dialogs
@st.dialog("Delete Chat")
def confirm_delete(cid):
    st.write("Delete this chat?")
    if st.button("Yes", use_container_width=True, type="primary"):
        del st.session_state.chat_sessions[cid]
        if st.session_state.current_chat_id == cid: st.session_state.current_chat_id = None
        st.rerun()

@st.dialog("Share Chat")
def show_share_link(cid, title):
    st.write(f"### {title}")
    st.code(f"https://techhawk-it.app/?chat={cid}")

@st.dialog("Rename Chat")
def rename_chat(cid, current_title):
    new_title = st.text_input("Rename", value=current_title)
    if st.button("Save"):
        st.session_state.chat_sessions[cid]['title'] = new_title; st.rerun()

# 5. Render Sidebar
render_sidebar(show_share_link, rename_chat, confirm_delete)

# 6. Main Chat Logic
st.markdown("<h1 class='centered-header'>TechHawk IT Help Desk</h1>", unsafe_allow_html=True)
# RESTORED SUBHEADER
st.markdown("<p class='centered-subheader'>Welcome to the Edwards Campus IT Assistant.</p>", unsafe_allow_html=True)

curr_id = st.session_state.current_chat_id
history = st.session_state.chat_sessions[curr_id]["messages"] if curr_id else []

for m in history:
    col_left, col_right = st.columns(2)
    with (col_right if m["role"] == "user" else col_left):
        with st.chat_message(m["role"]): st.markdown(m["content"])

if user_query := st.chat_input("Ask an IT question..."):
    if not curr_id:
        curr_id = str(uuid.uuid4())
        st.session_state.chat_sessions[curr_id] = {"title": user_query[:30], "pinned": False, "messages": []}
        st.session_state.current_chat_id = curr_id
    
    st.session_state.chat_sessions[curr_id]["messages"].append({"role": "user", "content": user_query})
    
    try:
        ai_answer = rag_chain.invoke(user_query) if rag_chain else "AI not configured."
    except:
        ai_answer = "The system is currently busy."
        
    st.session_state.chat_sessions[curr_id]["messages"].append({"role": "assistant", "content": ai_answer})
    st.rerun()