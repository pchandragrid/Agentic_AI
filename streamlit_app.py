import time
import streamlit as st

from app.agent import ask_agent

# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------

st.set_page_config(
    page_title="Nexus AI Engine",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------------------------------
# CSS INJECTION - PREMIUM DARK THEME
# ---------------------------------------------------

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&family=Inter:wght@300;400;500;600&display=swap');

/* Global Reset & Background */
html, body, [class*="css"] {
    background-color: #050509 !important;
    background-image: 
        radial-gradient(circle at 15% 50%, rgba(99, 102, 241, 0.08), transparent 25%),
        radial-gradient(circle at 85% 30%, rgba(168, 85, 247, 0.08), transparent 25%);
    background-attachment: fixed;
    color: #f8fafc !important;
    font-family: 'Inter', sans-serif !important;
}

/* Top Padding Adjustment */
.block-container {
    padding-top: 3rem !important;
    max-width: 900px !important;
}

/* Typography */
h1, h2, h3, h4, h5, h6 {
    font-family: 'Outfit', sans-serif !important;
    color: #ffffff !important;
    letter-spacing: -0.5px;
}

/* Custom Header */
.glow-title {
    font-family: 'Outfit', sans-serif;
    font-size: 56px;
    font-weight: 800;
    background: linear-gradient(135deg, #818cf8 0%, #c084fc 50%, #f472b6 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    text-align: center;
    margin-bottom: 5px;
    letter-spacing: -1.5px;
    animation: fadeIn 1s ease-out;
}

.sub-title {
    text-align: center;
    font-family: 'Inter', sans-serif;
    color: #94a3b8;
    font-size: 18px;
    font-weight: 400;
    margin-bottom: 40px;
    letter-spacing: 0.5px;
    animation: fadeIn 1.2s ease-out;
}

/* Sidebar Styling */
section[data-testid="stSidebar"] {
    background: rgba(10, 10, 15, 0.6) !important;
    backdrop-filter: blur(20px) !important;
    -webkit-backdrop-filter: blur(20px) !important;
    border-right: 1px solid rgba(255, 255, 255, 0.05);
}

section[data-testid="stSidebar"] .block-container {
    padding-top: 2rem !important;
}

/* Feature Tags in Sidebar */
.feature-tag {
    display: inline-block;
    padding: 8px 16px;
    background: rgba(139, 92, 246, 0.08);
    border: 1px solid rgba(139, 92, 246, 0.2);
    border-radius: 30px;
    font-size: 13px;
    font-weight: 500;
    color: #d8b4fe;
    margin: 4px;
    transition: all 0.3s ease;
    cursor: default;
}
.feature-tag:hover {
    background: rgba(139, 92, 246, 0.15);
    border-color: rgba(139, 92, 246, 0.4);
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(139, 92, 246, 0.15);
}

/* Chat Input Container */
[data-testid="stChatInput"] {
    background: rgba(15, 23, 42, 0.6) !important;
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
    border-radius: 24px !important;
    backdrop-filter: blur(16px) !important;
    -webkit-backdrop-filter: blur(16px) !important;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3) !important;
    padding: 4px !important;
    transition: all 0.3s ease;
}
[data-testid="stChatInput"]:focus-within {
    border-color: rgba(139, 92, 246, 0.5) !important;
    box-shadow: 0 8px 32px rgba(139, 92, 246, 0.2) !important;
}
[data-testid="stChatInput"] textarea {
    color: #ffffff !important;
}

/* Native Code Blocks */
pre {
    background: rgba(2, 6, 23, 0.8) !important;
    border: 1px solid rgba(255, 255, 255, 0.05) !important;
    border-radius: 12px !important;
    box-shadow: 0 4px 16px rgba(0,0,0,0.2) !important;
}
code {
    font-family: 'JetBrains Mono', 'Courier New', monospace !important;
    color: #93c5fd !important;
    background: transparent !important;
}

/* Animations */
@keyframes slideUpFade {
    from { opacity: 0; transform: translateY(20px); }
    to { opacity: 1; transform: translateY(0); }
}
@keyframes fadeIn {
    from { opacity: 0; }
    to { opacity: 1; }
}

/* Hide Streamlit Junk */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}

</style>
""", unsafe_allow_html=True)


# ---------------------------------------------------
# HEADER
# ---------------------------------------------------

st.markdown('<div class="glow-title">Nexus AI Engine</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Advanced Multimodal Autonomous Research Agent</div>', unsafe_allow_html=True)


# ---------------------------------------------------
# SIDEBAR
# ---------------------------------------------------

with st.sidebar:
    st.markdown("<h2 style='font-size: 20px; margin-bottom: 10px; color: #e2e8f0;'>⚙️ Engine Settings</h2>", unsafe_allow_html=True)
    max_iterations = st.slider(
        "Critique Iterations", 
        1, 5, 2, 
        help="Higher values increase research depth but take longer to process."
    )

    st.markdown("<hr style='border-color: rgba(255,255,255,0.05); margin: 24px 0;'>", unsafe_allow_html=True)

    st.markdown("<h2 style='font-size: 20px; margin-bottom: 16px; color: #e2e8f0;'>⚡ Capabilities</h2>", unsafe_allow_html=True)

    st.markdown("""
    <div style='margin-bottom: 10px;'>
        <div class="feature-tag">🔍 RAG Pipeline</div>
        <div class="feature-tag">⚡ FAISS Retrieval</div>
        <div class="feature-tag">🌐 Web Search</div>
        <div class="feature-tag">📈 Financial Data</div>
        <div class="feature-tag">📰 A2A News Agent</div>
        <div class="feature-tag">🧠 Critique Loop</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<hr style='border-color: rgba(255,255,255,0.05); margin: 24px 0;'>", unsafe_allow_html=True)

    st.markdown("<h3 style='font-size: 16px; color: #94a3b8;'>Suggested Queries</h3>", unsafe_allow_html=True)
    st.markdown("""
    <div style='font-size: 13px; color: #cbd5e1; line-height: 1.8; margin-left: 10px;'>
    • Latest AI news today<br>
    • Generate markdown report on AI trends<br>
    • What are Bitcoin risks?<br>
    • Compare Amazon and AI startup culture<br>
    • Write scalable scheduler in Python
    </div>
    """, unsafe_allow_html=True)


# ---------------------------------------------------
# SESSION STATE
# ---------------------------------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []


# ---------------------------------------------------
# DISPLAY CHAT HELPERS
# ---------------------------------------------------

def render_user_message(content):
    escaped_content = content.replace('\n', '<br>')
    st.markdown(
        f"""
        <div style="display: flex; justify-content: flex-end; margin-bottom: 30px; animation: slideUpFade 0.4s ease-out forwards;">
            <div style="background: linear-gradient(135deg, #6366f1 0%, #a855f7 100%); color: #ffffff; padding: 16px 24px; border-radius: 24px 24px 4px 24px; max-width: 80%; box-shadow: 0 8px 24px rgba(99, 102, 241, 0.25); font-family: 'Inter', sans-serif; line-height: 1.6; font-size: 15px; letter-spacing: 0.2px;">
                {escaped_content}
            </div>
            <div style="width: 38px; height: 38px; border-radius: 50%; background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1); display: flex; align-items: center; justify-content: center; margin-left: 16px; flex-shrink: 0; box-shadow: 0 4px 12px rgba(0,0,0,0.2);">👤</div>
        </div>
        """,
        unsafe_allow_html=True
    )

def render_assistant_header():
    st.markdown("""
    <div style="display: flex; align-items: center; margin-bottom: 12px; animation: fadeIn 0.5s ease-out;">
        <div style="width:38px; height:38px; border-radius:50%; background:linear-gradient(135deg, #3b82f6, #8b5cf6); display:flex; align-items:center; justify-content:center; margin-right:16px; box-shadow:0 0 15px rgba(139,92,246,0.4); font-size: 18px;">✨</div>
        <span style="font-weight: 600; color: #c084fc; font-family: 'Outfit', sans-serif; font-size: 17px; letter-spacing: 0.5px;">Nexus Engine</span>
    </div>
    """, unsafe_allow_html=True)

def render_assistant_separator():
    st.markdown("<hr style='border: none; border-bottom: 1px solid rgba(255,255,255,0.05); margin: 30px 0;'>", unsafe_allow_html=True)


# ---------------------------------------------------
# DISPLAY HISTORY
# ---------------------------------------------------

for msg in st.session_state.messages:
    if msg["role"] == "user":
        render_user_message(msg["content"])
    else:
        render_assistant_header()
        st.markdown(msg["content"])
        render_assistant_separator()


# ---------------------------------------------------
# CHAT INPUT & GENERATE RESPONSE
# ---------------------------------------------------

query = st.chat_input("Ask Nexus to research anything...")

if query:
    # Save & display user msg
    st.session_state.messages.append({"role": "user", "content": query})
    render_user_message(query)

    render_assistant_header()
    response_container = st.empty()
    full_response = ""

    with st.spinner("Initiating autonomous workflow..."):
        try:
            response = ask_agent(query, max_iterations=max_iterations)

            # Stream response (simulated streaming effect for UI)
            for chunk in response.split():
                full_response += chunk + " "
                response_container.markdown(full_response + "▌")
                time.sleep(0.015)

            # Final render
            response_container.markdown(response)
            render_assistant_separator()

            # Save assistant response
            st.session_state.messages.append({"role": "assistant", "content": response})

        except Exception as e:
            st.error(f"Engine Fault: {str(e)}")