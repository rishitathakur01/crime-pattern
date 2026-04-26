import streamlit as st
import pandas as pd
import os
import time
from langchain_community.document_loaders import DataFrameLoader
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

# Configuration
CHROMA_PATH = "chroma_db"
DATA_PATH = "crime_data.csv"

st.set_page_config(page_title="AI Crime Analyzer", page_icon="🕵️", layout="wide")

# Custom CSS for aesthetics
st.markdown("""
<style>
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        border-radius: 5px;
        border: none;
        padding: 10px 24px;
        transition: all 0.3s ease 0s;
    }
    .stButton>button:hover {
        background-color: #45a049;
        transform: translateY(-2px);
        box-shadow: 0px 5px 15px rgba(76, 175, 80, 0.4);
    }
</style>
""", unsafe_allow_html=True)

# Define the local embedding model
@st.cache_resource
def get_embeddings():
    return HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

# Initialize and cache the vector database
@st.cache_resource
def init_vector_db():
    embeddings = get_embeddings()
    if os.path.exists(CHROMA_PATH) and os.listdir(CHROMA_PATH):
        # Load existing DB
        db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embeddings)
        return db
    else:
        # Create new DB from CSV
        if not os.path.exists(DATA_PATH):
            st.error(f"Data file '{DATA_PATH}' not found. Please run generate_data.py first.")
            st.stop()
            
        df = pd.read_csv(DATA_PATH)
        # Create a combined text field for better semantic search
        df['page_content'] = df.apply(lambda row: f"Incident ID: {row['Incident_ID']}. Type: {row['Crime_Type']}. Location: {row['Location']}. Description: {row['Description']}. Date: {row['Date_Time']}", axis=1)
        
        loader = DataFrameLoader(df, page_content_column="page_content")
        documents = loader.load()
        
        st.info("Initializing Vector Database. This may take a minute as it downloads the embedding model and creates embeddings...")
        db = Chroma.from_documents(documents, embeddings, persist_directory=CHROMA_PATH)
        return db

def generate_mock_insight(query, docs):
    """Simulates a Generative AI model analyzing the retrieved documents."""
    time.sleep(1.5) # Simulate processing time
    
    if not docs:
        return "No relevant past incidents found to analyze."
    
    locations = list(set([doc.metadata.get('Location', 'Unknown') for doc in docs]))
    crime_types = list(set([doc.metadata.get('Crime_Type', 'Unknown') for doc in docs]))
    
    insight = f"### 🧠 AI Generated Analysis & Risk Assessment\n\n"
    insight += f"**Contextual Pattern Match**: The system analyzed your query against historical records and found **{len(docs)} highly similar incidents**.\n\n"
    
    insight += f"#### Key Findings:\n"
    insight += f"- **Common Crime Types Identified**: {', '.join(crime_types)}\n"
    insight += f"- **High-Risk Zones**: {', '.join(locations)}\n\n"
    
    insight += f"#### Behavioral & Trend Analysis:\n"
    insight += f"Based on the semantic similarity to past events, the current scenario exhibits characteristics commonly associated with historical **{crime_types[0].lower()}** operations in the region. Past data suggests these incidents frequently cluster around specific geographic zones or timeframes as seen in the supporting evidence.\n\n"
    
    insight += f"#### Actionable Recommendations:\n"
    insight += f"1. **Deploy Preventive Measures**: Increase surveillance and visibility in **{locations[0]}** during suspected high-risk hours.\n"
    insight += f"2. **Community Alert**: Consider issuing an advisory for residents regarding recent {crime_types[0].lower()} trends.\n"
    insight += f"3. **Investigative Focus**: Cross-reference new leads with evidence from past incidents (e.g., Incident ID: {docs[0].metadata.get('Incident_ID', 'N/A')}).\n"
    
    return insight

# Application UI
st.title("🕵️ AI Crime Pattern Analysis System")
st.markdown("Analyze past crime data and identify potential risk patterns using Similarity Search & Generative AI.")

db = init_vector_db()

st.divider()

col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("🔍 Scenario Input")
    st.markdown("Describe a suspicious scenario, recent event, or specific crime type/location to analyze risks.")
    query = st.text_area("Enter scenario details:", height=150, placeholder="e.g., Suspicious activity involving a stolen vehicle late at night in Shimla, Himachal Pradesh.")
    analyze_btn = st.button("Analyze Scenario", use_container_width=True)

with col2:
    if analyze_btn and query:
        with st.spinner("Analyzing patterns using Vector Database and Generative AI..."):
            # Similarity Search
            results = db.similarity_search(query, k=3)
            
            # Generate AI Insights
            insights = generate_mock_insight(query, results)
            
            st.success("Analysis Complete!")
            st.markdown(insights)
            
            st.subheader("📂 Supporting Historical Evidence")
            for i, doc in enumerate(results):
                with st.expander(f"Incident Match #{i+1}: {doc.metadata.get('Crime_Type')} in {doc.metadata.get('Location')}"):
                    st.markdown(f"**Date/Time**: {doc.metadata.get('Date_Time')}")
                    st.markdown(f"**Description**: {doc.metadata.get('Description')}")
                    st.markdown(f"**Incident ID**: `{doc.metadata.get('Incident_ID')}`")
    elif analyze_btn and not query:
        st.warning("Please enter a scenario to analyze.")
    elif not analyze_btn:
        st.info("👈 Enter a scenario on the left and click 'Analyze Scenario'.")

st.divider()
st.caption("Note: This system uses a local vector database (ChromaDB) and a simulated Generative AI model for demonstration purposes (no API keys required).")
