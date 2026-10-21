import streamlit as st
import os
from summarizer import LocalDocumentSummarizer

st.set_page_config(page_title="Local AI Document Summarizer & Q&A Assistant", page_icon="📄", layout="wide")

st.title("📁 Local AI Document Summarizer & Q&A Assistant")
st.caption("A local, private, and secure AI app powered by Ollama, LangChain, and scikit-learn.")

@st.cache_resource
def get_summarizer():
    return LocalDocumentSummarizer(model_name="llama3")

summarizer = get_summarizer()

if "vector_ready" not in st.session_state:
    st.session_state.vector_ready = False

summary_option = st.selectbox(
    "Select Summary Format:",
    ("Bullet Points", "Executive Summary", "Detailed Report")
)

uploaded_file = st.file_uploader("Upload a PDF document to summarize and ask questions about", type=["pdf"])

if uploaded_file is not None:
    temp_dir = "temp_files"
    os.makedirs(temp_dir, exist_ok=True)
    temp_path = os.path.join(temp_dir, uploaded_file.name)
    
    with open(temp_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.success(f"File uploaded: **{uploaded_file.name}**")

    if st.button("Summarize Document and Prepare for Q&A", type="primary"):
        with st.spinner("Analyzing document and creating local vector database..."):
            try:
                split_docs = summarizer.load_and_split_pdf(temp_path)
                st.info(f"Document split into **{len(split_docs)}** parts.")

                summary = summarizer.summarize(split_docs, summary_type=summary_option)
                st.session_state.current_summary = summary

                summarizer.setup_vector_db(split_docs)
                st.session_state.vector_ready = True

                st.success("Document processed successfully! You can now ask questions about it.")

            except Exception as e:
                st.error(f"An error occurred: {str(e)}")

    if "current_summary" in st.session_state:
        st.markdown(f"### 📝 Created Summary ({summary_option}):")
        st.write(st.session_state.current_summary)

        st.download_button(
            label="Download Summary (.txt)",
            data=st.session_state.current_summary,
            file_name=f"{uploaded_file.name}_summary.txt",
            mime="text/plain"
        )

    if st.session_state.vector_ready:
        st.markdown("---")
        st.markdown("### 🤖 Ask a Question about the Document")
        user_question = st.text_input("Ask a question about the uploaded document:")
        if user_question:
            with st.spinner("Analyzing document and generating answer..."):
                answer = summarizer.ask_question(user_question)
                st.markdown("**Generated Answer:**")
                st.write(answer)

    if os.path.exists(temp_path):
        os.remove(temp_path)