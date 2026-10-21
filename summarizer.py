import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import ChatOllama
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class LocalDocumentSummarizer:
    def __init__(self, model_name="llama3"):
        # Ollama connection address sensitive to Docker environment or local host
        ollama_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
        self.llm = ChatOllama(model=model_name, temperature=0.2, base_url=ollama_url)
        self.chunks = []

    def load_and_split_pdf(self, file_path):
        loader = PyPDFLoader(file_path)
        docs = loader.load()
        
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=150
        )
        split_docs = text_splitter.split_documents(docs)
        self.chunks = [doc.page_content for doc in split_docs]
        return split_docs

    def summarize(self, docs, summary_type="Bullet Points"):
        full_text = "\n".join([doc.page_content for doc in docs])
        
        if summary_type == "Executive Summary":
            instruction = "Summarize this text into a concise executive summary of at most 3-4 clear sentences in English."
        elif summary_type == "Bullet Points":
            instruction = "Summarize this text into an organized English bullet-point list highlighting the most important points and findings."
        else:
            instruction = "Summarize this text comprehensively into a detailed report with subheadings in English, without skipping any details."

        prompt = f"""
        {instruction}
        
        Text to be reviewed:
        {full_text[:12000]} 
        
        SUMMARY:
        """
        
        response = self.llm.invoke(prompt)
        return response.content

    def setup_vector_db(self, docs):
        """Prepares text chunks for TF-IDF based search."""
        self.chunks = [doc.page_content for doc in docs]

    def ask_question(self, question):
        """Searches among text chunks using TF-IDF and cosine similarity to provide context to the LLM."""
        if not self.chunks:
            return "Please upload a document and generate a summary first."
        
        # TF-IDF vectorization and similarity calculation
        vectorizer = TfidfVectorizer().fit(self.chunks)
        chunk_vectors = vectorizer.transform(self.chunks)
        question_vector = vectorizer.transform([question])
        
        similarities = cosine_similarity(question_vector, chunk_vectors).flatten()
        
        # Select the top 3 chunks with the highest similarity
        top_indices = similarities.argsort()[-3:][::-1]
        relevant_chunks = [self.chunks[i] for i in top_indices]
        
        context = "\n\n".join(relevant_chunks)
        
        prompt = f"""
        Answer the question using the context (document chunks) provided below. If the answer is not in the context, say "The answer to this question is not found in the uploaded document."
        
        Context:
        {context}
        
        Question: {question}
        
        ENGLISH ANSWER:
        """
        
        response = self.llm.invoke(prompt)
        return response.content