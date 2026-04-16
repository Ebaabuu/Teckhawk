import streamlit as st

def apply_custom_styles():
    st.markdown("""
    <style>
    .stAppDeployButton {display: none !important;}
    @keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
    [data-testid="stChatMessage"] { animation: fadeIn 0.6s ease-out forwards; }
    .main .block-container { max-width: 1100px; }

    /* SIDEBAR WIDTH & BUTTONS */
    [data-testid="stSidebarViewPort"] { min-width: 250px !important; }
    [data-testid="stSidebar"] .stButton > button {
        border-radius: 20px !important;
        background-color: #e0e0e0 !important;
        color: black !important;
        border: none !important;
        height: 40px !important;
        text-align: left !important;
        width: 100% !important;
        padding-left: 15px !important;
        padding-right: 45px !important; 
        display: block !important; 
        line-height: 40px !important; 
        white-space: nowrap !important;
        overflow: hidden !important;
        text-overflow: ellipsis !important;
    }

     /* THE POPOVER (THREE DOTS) */
    [data-testid="stSidebar"] div[data-testid="stPopover"] {
        position: absolute !important;
        right: 12px !important;
        margin-top: -55px !important; 
        width: 30px !important;
        height: 40px !important;
        z-index: 99 !important;
        opacity: 0; 
        pointer-events: none; 
        transition: opacity 0.2s ease-in-out;
    }
    [data-testid="stVerticalBlock"] > div:hover div[data-testid="stPopover"] {
        opacity: 1 !important;
        pointer-events: auto !important;
    }
    [data-testid="stSidebar"] [data-testid="stPopover"] svg { display: none !important; }
    [data-testid="stSidebar"] [data-testid="stPopover"] button div:last-child { display: none !important; }
    [data-testid="stSidebar"] [data-testid="stPopover"] button::before {
        content: "⋮"; font-size: 22px; color: #444; font-weight: bold;
    }
    [data-testid="stSidebar"] [data-testid="stPopover"] button {
        background: transparent !important; border: none !important; box-shadow: none !important;
        width: 30px !important; height: 40px !important;
    }
                
    /* CHAT BUBBLES */
    [data-testid="stChatMessage"]:has([data-testid="stChatMessageUserAvatar"]) { flex-direction: row-reverse !important; }
    </style>
    """, unsafe_allow_html=True)

    