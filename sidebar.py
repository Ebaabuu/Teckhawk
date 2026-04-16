import streamlit as st

def render_sidebar(show_share_link, rename_chat, confirm_delete):
    with st.sidebar:
        st.markdown("<h1 style='text-align: center;'>History</h1>", unsafe_allow_html=True)
        
        # New Chat Button
        if st.button("➕      New Chat", use_container_width=True):
            st.session_state.current_chat_id = None
            st.rerun()
            
        # Search Bar
        search_q = st.text_input("🔍 Search", label_visibility="collapsed", placeholder="🔍    Search", key="sidebar_search")
        st.divider()

        # Sort: Pinned first
        sorted_sessions = sorted(st.session_state.chat_sessions.items(), key=lambda x: (not x[1]['pinned']))

        for cid, data in sorted_sessions:
            if search_q.lower() in data['title'].lower():
                with st.container():
                    pin_marker = "📌 " if data['pinned'] else ""
                    short_title = (data['title'][:18] + "...") if len(data['title']) > 18 else data['title']
                    
                    # Main History Pill
                    if st.button(f"{pin_marker}{short_title}", key=f"b_{cid}", use_container_width=True):
                        st.session_state.current_chat_id = cid
                        st.rerun()
                    
                    # The Tool Menu (Three Dots)
                    with st.popover(""):
                        # 1. Share
                        if st.button("➦ Share Chat", key=f"s_{cid}", use_container_width=True):
                            show_share_link(cid, data['title'])
                        
                        # 2. Pin/Unpin Toggle
                        if data['pinned']:
                            if st.button("🚫 Unpin", key=f"p_{cid}", use_container_width=True):
                                st.session_state.chat_sessions[cid]['pinned'] = False
                                st.rerun()
                        else:
                            if st.button("📌 Pin Chat", key=f"p_{cid}", use_container_width=True):
                                st.session_state.chat_sessions[cid]['pinned'] = True
                                st.rerun()
                        
                        # 3. Rename
                        if st.button("✏️ Rename", key=f"r_{cid}", use_container_width=True):
                            rename_chat(cid, data['title'])
                        
                        # 4. Delete
                        if st.button("🗑️ Delete", key=f"del_{cid}", use_container_width=True):
                            confirm_delete(cid)