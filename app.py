import streamlit as st
import json
from google import genai
from google.genai import types
from PIL import Image

# ==========================================
# 1. PAGE CONFIGURATION & THEME CUSTOMIZATION
# ==========================================
st.set_page_config(
    page_title="Local-Lore Storyteller",
    page_icon="🏰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom injection for a clean, modern card-based layout and vibrant highlights
st.markdown("""
    <style>
    .main-header {
        font-size: 2.8rem;
        font-weight: 800;
        background: linear-gradient(135deg, #FFD700, #FF8C00);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.1rem;
        color: #A0A0A0;
        margin-bottom: 2rem;
    }
    .feature-card {
        background-color: #1E1E24;
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 5px solid #FFD700;
        margin-bottom: 1rem;
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 2. CLIENT INITIALIZATION & SESSION STATE
# ==========================================
# Hardcoding the key directly for guaranteed hackathon deployment connection
try:
    client = genai.Client(api_key="")
except Exception as e:
    st.error(f"Failed to initialize Gemini Client: {e}")
    st.stop()

# Initialize session storage for the chat system in Tab 2
if "visual_chat_history" not in st.session_state:
    st.session_state.visual_chat_history = []
if "analyzed_image_target" not in st.session_state:
    st.session_state.analyzed_image_target = None

# ==========================================
# 3. SIDEBAR / GLOBAL CONTROLS
# ==========================================
with st.sidebar:
    st.markdown("### 🌐 Global Settings")
    language = st.selectbox("Output Language", ["English", "Turkish", "Urdu", "Arabic", "Spanish"])

# Main Screen Titles
st.markdown('<div class="main-header">🏰 Local-Lore Storyteller</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Bringing cultural heritage and physical history to life using Google Gemini AI</div>', unsafe_allow_html=True)

# Split features into clear, scannable Tabs
tab1, tab2 = st.tabs(["⚡ Generator & Quiz Mode", "👁️ Multimodal Image Chat"])


# ==========================================
# 4. TAB 1: STORY GENERATOR & INTERACTIVE QUIZ
# ==========================================
with tab1:
    st.markdown("### Craft a History Adventure")
    
    # Grid layout for inputs
    col1, col2 = st.columns(2)
    with col1:
        # Replaced selectbox with a free-form text input
        landmark = st.text_input(
            "Target Landmark, Figure, or Historic Event:",
            placeholder="e.g., Ankara Castle, Mohenjo-daro, The Battle of Gallipoli..."
        )
    with col2:
        persona = st.selectbox(
            "Storyteller Character Persona:",
            [
                "Cyberpunk Time-Traveler from 2150", 
                "Friendly Medieval Knight Guarding the Gates", 
                "Curious Galactic Historian", 
                "Wise Ancient Spirit of the Landmark"
            ]
        )

    if st.button("Generate Lore Adventure ✨", type="primary", use_container_width=True):
        with st.spinner("Gemini is assembling historical data and drafting the narrative..."):
            
            # Formulating strict JSON schema prompt instructions
            prompt = f"""
            Write a highly engaging, short educational story for students about the historical topic: {landmark}.
            The story narrative must be told entirely through the persona of a {persona}.
            The entire response language must be strictly in {language}.
            
            Return the output strictly as a valid JSON object matching this schema blueprint:
            {{
                "title": "Title of the story",
                "story": "The complete narrative goes here",
                "quiz_question": "A multiple-choice question testing details mentioned in the story",
                "quiz_options": ["Option A", "Option B", "Option C"],
                "correct_answer_index": "0 or 1 or 2 as a string index pointing to the right choice"
            }}
            """
            
            try:
                # Execute API call forcing JSON response parsing
                response = client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        response_mime_type="application/json",
                    ),
                )
                
                # Cache response data in session state to maintain integrity during quiz re-runs
                st.session_state.quiz_data = json.loads(response.text)
                
            except Exception as error:
                st.error(f"Generation Interface Failed: {error}")

    # Display the generated content if it exists in state
    if "quiz_data" in st.session_state:
        data = st.session_state.quiz_data
        
        st.markdown(f"## {data['title']}")
        st.markdown(f'<div class="feature-card">{data["story"]}</div>', unsafe_allow_html=True)
        
        st.divider()
        st.markdown("### 🧠 Interactive Challenge")
        st.write(data['quiz_question'])
        
        # User choices radio setup
        user_selection = st.radio("Select your answer:", data['quiz_options'], key="quiz_radio")
        
        if st.button("Verify Answer ✅"):
            target_correct_string = data['quiz_options'][int(data['correct_answer_index'])]
            if user_selection == target_correct_string:
                st.balloons()
                st.success("Brilliant! You mastered this piece of history.")
            else:
                st.error(f"Incorrect. The history sheets indicate the answer is: {target_correct_string}")


# ==========================================
# 5. TAB 2: MULTIMODAL VISUAL ANALYSIS & CHAT
# ==========================================
with tab2:
    st.markdown("### Upload Historic Photo Analyzer")
    st.caption("Drop any photo of an ancient structure, painting, or museum artifact to detect its history and chat interactively.")
    
    uploaded_file = st.file_uploader("Choose a historical image...", type=["jpg", "jpeg", "png"])
    
    if uploaded_file is not None:
        # Load and handle image formats safely via PIL
        image_content = Image.open(uploaded_file)
        
        # UI Split layout: Left column shows photo, Right column handles initial breakdown
        v_col1, v_col2 = st.columns([1, 1])
        
        with v_col1:
            st.image(image_content, caption="Uploaded Target Specimen", use_container_width=True)
            
        with v_col2:
            if st.button("Scan & Analyze Image 🔍", use_container_width=True, type="primary"):
                with st.spinner("Gemini Multimodal engine parsing image layers..."):
                    
                    analysis_prompt = f"""
                    Identify what historical object, landmark, or artwork is in this image. 
                    Provide a comprehensive summary detailing its approximate age, origins, and cultural significance.
                    Respond in {language}.
                    """
                    
                    try:
                        # Direct ingestion of text list along with the raw PIL Image object
                        response = client.models.generate_content(
                            model='gemini-2.5-flash',
                            contents=[analysis_prompt, image_content]
                        )
                        
                        st.session_state.initial_analysis = response.text
                        st.session_state.analyzed_image_target = image_content
                        # Clear history for a fresh image upload swap
                        st.session_state.visual_chat_history = []
                        
                    except Exception as img_err:
                        st.error(f"Vision Processing Error: {img_err}")
            
            if "initial_analysis" in st.session_state:
                st.markdown("### 📊 Historical Breakdown")
                st.write(st.session_state.initial_analysis)

        # Chat interface beneath the analysis panel once image is indexed
        if st.session_state.analyzed_image_target is not None:
            st.divider()
            st.markdown("### 💬 Ask Follow-Up Questions About This Image")
            
            # Display current conversation history logs
            for message in st.session_state.visual_chat_history:
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])
            
            # Collect fresh chat entry inputs
            if user_chat_input := st.chat_input("Ask something else (e.g., 'What engineering methods were used to build this?')"):
                
                # Append user prompt log to display instantly
                with st.chat_message("user"):
                    st.markdown(user_chat_input)
                st.session_state.visual_chat_history.append({"role": "user", "content": user_chat_input})
                
                # Process reply using current query context combined with the active source image
                with st.chat_message("assistant"):
                    with st.spinner("Thinking..."):
                        try:
                            chat_prompt = f"""
                            The user is asking a follow-up question regarding the historical image provided earlier.
                            Question: {user_chat_input}
                            Provide an accurate response based on historical facts in {language}.
                            """
                            
                            chat_response = client.models.generate_content(
                                model='gemini-2.5-flash',
                                contents=[chat_prompt, st.session_state.analyzed_image_target]
                            )
                            
                            st.markdown(chat_response.text)
                            st.session_state.visual_chat_history.append({"role": "assistant", "content": chat_response.text})
                        except Exception as chat_api_err:
                            st.error(f"Chat Interface Failed: {chat_api_err}")