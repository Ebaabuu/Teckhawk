import streamlit as st
import uuid
import time
from sidebar import render_sidebar
from styles import apply_custom_styles
from brain import load_rag_chain
from langchain_core.messages import HumanMessage, AIMessage

# ==========================================
# System Initialization & UI Configuration
# ==========================================
st.set_page_config(page_title="TechHawk IT Assistant", layout="wide")
apply_custom_styles()

# Render the sidebar model selector for benchmarking capabilities
st.sidebar.markdown("### Engine Benchmark")
selected_model = st.sidebar.selectbox(
    "Active LLM:",
    ("Gemini 2.5 Flash", "ChatGPT (GPT-5.4 Mini)", "Ollama (Local)"),
    index=0
)
st.sidebar.divider()

# Load the Retrieval-Augmented Generation (RAG) chain. 
# Triggers a reload only if the user switches the active LLM.
if "rag_chain" not in st.session_state or st.session_state.get("current_model") != selected_model:
    with st.spinner(f"Booting {selected_model}..."):
        st.session_state.rag_chain = load_rag_chain(selected_model)
        st.session_state.current_model = selected_model


# ==========================================
# Session State Management
# ==========================================
# Ensure history dictionary and active chat tracker exist on first load
if "chat_sessions" not in st.session_state: st.session_state.chat_sessions = {}
if "current_chat_id" not in st.session_state: st.session_state.current_chat_id = None

# ==========================================
# Modal Dialog Definitions
# ==========================================
@st.dialog("Delete Chat")
def confirm_delete(cid):
    # Prompt user for confirmation before permanently removing a chat from session state.
    st.write("Do you want to delete this chat?")
    c1, c2 = st.columns(2) # Side-by-side layout
    with c1:
        if st.button("Yes", use_container_width=True, type="primary"):
            del st.session_state.chat_sessions[cid]
            if st.session_state.current_chat_id == cid: st.session_state.current_chat_id = None
            st.rerun()
    with c2:
        if st.button("No", use_container_width=True): st.rerun()

@st.dialog("Share Chat")
def show_share_link(cid, title):
    # Generate and display a shareable URL for the specific chat session.
    st.write(f"### {title}")
    share_url = f"https://techhawk-it-assistant.streamlit.app/?chat={cid}"
    st.code(share_url, language="text")
    if st.button("Close", use_container_width=True): st.rerun()

@st.dialog("Rename Chat")
def rename_chat(cid, current_title):
    # Allow the user to overwrite the auto-generated or current chat title.
    st.write("Enter a new name for this chat:")
    new_title = st.text_input("Chat Name", value=current_title, label_visibility="collapsed")
    c1, c2 = st.columns(2) # Side-by-side layout
    with c1:
        if st.button("Save", use_container_width=True, type="primary"):
            if new_title.strip():
                st.session_state.chat_sessions[cid]['title'] = new_title.strip()
                st.rerun()
    with c2:
        if st.button("Cancel", use_container_width=True): st.rerun()

# ==========================================
# Main Interface Rendering
# ==========================================
# Render the sidebar navigation tools
render_sidebar(show_share_link, rename_chat, confirm_delete)

# Retrieve the message history for the currently active chat
curr_id = st.session_state.current_chat_id
history = st.session_state.chat_sessions[curr_id]["messages"] if curr_id else []

# Display landing page if no chat is active
if not history:
    st.markdown("<div style='text-align: center; margin-top: 50px;'><h1>TechHawk IT Help Desk</h1><p>Welcome to the secure Edwards Campus IT Assistant.</p></div>", unsafe_allow_html=True)

# Render chat bubbles dynamically based on role
for m in history:
    col_l, col_r = st.columns(2)
    if m["role"] == "user":
        with col_r:
            with st.chat_message("user", avatar="user_icon.png"):
                st.markdown(m["content"])
                if m.get("file"): st.caption(f"File: {m['file']}")
    else:
        with col_l:
            with st.chat_message("assistant", avatar="hawk_icon.png"): st.markdown(m["content"])

# ==========================================
# Input Handling & RAG Execution
# ==========================================
# Await user prompt or file upload
if user_input := st.chat_input("Ask an IT question...", accept_file="multiple"):
    text = user_input["text"]
    files = user_input["files"]

    # Auto-generate a title based on text or filename if creating a new chat
    title = text[:40] if text.strip() else (files[0].name[:40] if files else "New Chat")
    
    # Initialize a new session record if one doesn't exist
    if not curr_id:
        curr_id = str(uuid.uuid4())
        st.session_state.chat_sessions[curr_id] = {"title": title, "pinned": False, "messages": []}
        st.session_state.current_chat_id = curr_id
    
    # Append the user's input to the active session history
    st.session_state.chat_sessions[curr_id]["messages"].append({
        "role": "user", "content": text if text.strip() else "[File Uploaded]", "file": files[0].name if files else None
    })
    st.rerun()

# Trigger the LLM if the last message in history belongs to the user
if curr_id and history and history[-1]["role"] == "user":
    with st.spinner("TechHawk is thinking..."):
        start_time = time.time()
        
        try:
            # Format conversational memory into LangChain message objects
            # Excludes the most recent query to prevent duplication in the prompt
            lc_history = []
            for msg in history[:-1]: 
                if msg["role"] == "user":
                    lc_history.append(HumanMessage(content=msg["content"]))
                else:
                    lc_history.append(AIMessage(content=msg["content"]))
            
            # Execute the retrieval and generation chain
            ai_answer = st.session_state.rag_chain.invoke({
                "input": history[-1]["content"],
                "chat_history": lc_history
            })
            
        except Exception as e:
            print(f"API Error encountered: {e}")
            ai_answer = "API Error: Check Terminal"
        
        # Enforce a minimum spinner duration for UX consistency
        elapsed = time.time() - start_time
        if elapsed < 1.5:
            time.sleep(1.5 - elapsed)
            
    # Append the AI's response to the history and refresh the UI
    st.session_state.chat_sessions[curr_id]["messages"].append({"role": "assistant", "content": ai_answer})
    st.rerun()