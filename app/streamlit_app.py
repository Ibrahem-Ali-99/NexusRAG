import streamlit as st
import os
from dotenv import load_dotenv
from rag_processor import MultimodalRAGProcessor
from pdf_handler import process_pdf_from_upload

load_dotenv()

st.set_page_config(
    page_title="NexusRAG",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 NexusRAG: Ask Questions About Your Documents")
st.write("Upload a PDF and ask questions about its content. The system understands both text and images.")

groq_api_key = os.environ.get("GROQ_API_KEY")

if not groq_api_key:
    st.warning("GROQ_API_KEY not found! Please add it to your secrets or a .env file.", icon="⚠️")
    st.stop()

if 'rag_system' not in st.session_state:
    st.session_state.rag_system = None
if 'processed' not in st.session_state:
    st.session_state.processed = False
if 'file_name' not in st.session_state:
    st.session_state.file_name = None

with st.sidebar:
    st.header("Setup")
    uploaded_file = st.file_uploader("Upload your PDF document", type="pdf")

    if uploaded_file is not None:
        if st.button("Process Document"):
            with st.spinner("Processing document... This may take a few minutes for the first run."):
                try:
                    st.session_state.rag_system = None
                    st.session_state.processed = False

                    rag_processor = MultimodalRAGProcessor()
                    
                    st.session_state.file_name = uploaded_file.name
                    chunks = process_pdf_from_upload(uploaded_file)
                    rag_processor.store_chunks(chunks)

                    st.session_state.rag_system = rag_processor
                    st.session_state.processed = True
                    st.success(f"Document '{st.session_state.file_name}' processed successfully!")
                except Exception as e:
                    st.error(f"An error occurred: {e}")
                    st.error("Please ensure your Groq API key is correct and models are accessible.")
    st.markdown("---")
    st.markdown(
        "Built by [Your Name](https://github.com/your-username) with Streamlit, Groq, and Hugging Face."
    )


if st.session_state.processed:
    st.info(f"Ready to answer questions about **{st.session_state.file_name}**.")
    
    question = st.text_input("Ask a question:", placeholder="e.g., What is the main idea of the Transformer model?")

    if question:
        with st.spinner("Retrieving context and generating answer..."):
            rag_system = st.session_state.rag_system
            if rag_system:
                context = rag_system.query_rag(question)
                answer = rag_system.generate_answer(question, context)

                st.subheader("Answer")
                st.write(answer)
                
                with st.expander("See Retrieved Context"):
                    st.text(context)
            else:
                st.error("RAG system is not initialized. Please process a document first.")
else:
    st.info("Please upload and process a PDF document to begin.")