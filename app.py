import streamlit as st
from google import genai
from google.genai import types

# --- 1. Page Configuration & Title ---
st.set_page_config(page_title="AI Delivery Hub PoC", layout="wide")
st.title("🚀 AI Delivery Hub — Next-Gen Multi-Role Ecosystem")
st.caption("Driving Delivery Efficiency Across Cross-Functional Teams")

# --- 2. Initialize Gemini Client ---
# Securely input API key via sidebar
api_key = st.sidebar.text_input("Enter Gemini API Key:", type="password")

if api_key:
    client = genai.Client(api_key=api_key)
else:
    st.sidebar.warning("Please enter your Gemini API Key to enable AI features.")

# --- 3. Initialize Shared Session State Memory ---
if 'consultant_output' not in st.session_state:
    st.session_state['consultant_output'] = ""
if 'dev_output' not in st.session_state:
    st.session_state['dev_output'] = ""

# --- 4. Sidebar Navigation ---
st.sidebar.header("Navigation")
role = st.sidebar.radio("Select Delivery Workspace View:", [
    "🧑‍💻 Functional Consultant", 
    "⚙️ Technical Developer", 
    "🧪 QA Specialist"
])

# ==========================================
# TAB 1: FUNCTIONAL CONSULTANT WORKSPACE
# ==========================================
if role == "🧑‍💻 Functional Consultant":
    st.header("Functional Consultant Workspace")
    st.subheader("Phase: Requirement Optimization & Gap Discovery")
    
    # Left/Right Column Layout
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### 📥 Human Input: Raw Discovery Notes")
        default_notes = (
            "Client wants a way to auto-route support tickets based on tier. Tier 1 is basic, Tier 3 is critical.\n"
            "High-value customers (VIPs) should automatically bypass Tier 1 and go straight to a premium queue.\n"
            "If a critical ticket sits for more than 2 hours without an update, email the support manager.\n"
            "The client mentioned they might want to sync this with an external billing system later."
        )
        user_notes = st.text_area("Paste unstructured scoping or client notes here:", value=default_notes, height=200)
        
        generate_btn = st.button("⚡ Run AI Thinking Partner Analysis")

    with col2:
        st.markdown("### 🤖 AI Agent Outputs")
        if generate_btn:
            if not api_key:
                st.error("API Key missing.")
            else:
                with st.spinner("Analyzing requirements and mapping blindspots..."):
                    # Define System Prompt
                    sys_instruction = (
                        "You are an expert Agile Delivery AI Engine acting as an interactive thinking partner. "
                        "First, provide a section named '### 🔍 AI CRITIQUE & BLINDSPOTS' flagging ambiguous items. "
                        "Second, provide a section named '### 📄 STRUCTURED USER STORIES' in standard Agile format."
                    )
                    
                    # Call Gemini
                    response = client.models.generate_content(
                        model='gemini-2.5-flash',
                        contents=user_notes,
                        config=types.GenerateContentConfig(system_instruction=sys_instruction)
                    )
                    
                    # Save to global memory and display
                    st.session_state['consultant_output'] = response.text
                    st.markdown(response.text)
        else:
            if st.session_state['consultant_output']:
                st.markdown(st.session_state['consultant_output'])
            else:
                st.info("Paste your notes on the left and click Generate to activate the thinking partner workflow.")

# ==========================================
# TAB 2: TECHNICAL DEVELOPER WORKSPACE
# ==========================================
elif role == "⚙️ Technical Developer":
    st.header("Technical Developer Workspace")
    st.subheader("Phase: Technical Solutioning & Architectural Risk Mapping")
    
    if not st.session_state['consultant_output']:
        st.warning("⚠️ No data available. Please run the Functional Consultant analysis in Tab 1 first to pass requirements down the delivery pipeline.")
    else:
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.markdown("### 📥 Inherited Context (From Consultant View)")
            st.info("The Developer Agent automatically reads the optimized user stories generated in the previous phase.")
            st.markdown(st.session_state['consultant_output'])
            
            dev_btn = st.button("⚙️ Generate Technical Blueprint")
            
        with col2:
            st.markdown("### 🤖 AI Technical Solution Blueprint")
            if dev_btn:
                with st.spinner("Mapping architectural schema and backend risks..."):
                    sys_instruction = (
                        "You are an expert Enterprise Solutions Architect. Analyze the provided user stories. "
                        "Output a section '### 🛠️ CONFIGURATION & SCHEMA STRATEGY' detailing generic backend data structures "
                        "and a section '### ⚠️ ARCHITECTURAL RISKS' detailing performance or integration bottlenecks."
                    )
                    response = client.models.generate_content(
                        model='gemini-1.5-flash',
                        contents=st.session_state['consultant_output'],
                        config=types.GenerateContentConfig(system_instruction=sys_instruction)
                    )
                    st.session_state['dev_output'] = response.text
                    st.markdown(response.text)
            else:
                if st.session_state['dev_output']:
                    st.markdown(st.session_state['dev_output'])

# ==========================================
# TAB 3: QA SPECIALIST WORKSPACE
# ==========================================
elif role == "🧪 QA Specialist":
    st.header("QA Specialist Workspace")
    st.subheader("Phase: Automated Test Script & Edge Case Generation")
    
    if not st.session_state['dev_output']:
        st.warning("⚠️ Technical context missing. Please generate the Technical Blueprint in Tab 2 first.")
    else:
        st.markdown("### 🤖 AI QA Validation Framework")
        if st.button("🧪 Generate Edge Cases & UAT Scripts"):
            with st.spinner("Compiling test matrix..."):
                combined_context = f"Requirements:\n{st.session_state['consultant_output']}\n\nTechnical Notes:\n{st.session_state['dev_output']}"
                sys_instruction = (
                    "You are a Lead QA Engineer. Generate an '### 🛑 EDGE-CASE MATRIX' for extreme boundary conditions "
                    "and a step-by-step '### 📝 USER ACCEPTANCE TESTING (UAT) SCRIPT'."
                )
                response = client.models.generate_content(
                    model='gemini-1.5-flash',
                    contents=combined_context,
                    config=types.GenerateContentConfig(system_instruction=sys_instruction)
                )
                st.markdown(response.text)
