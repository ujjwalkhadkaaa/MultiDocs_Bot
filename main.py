import streamlit as st
from langchain.chains import ConversationalRetrievalChain
from langchain_community.document_loaders import PyPDFLoader, TextLoader, UnstructuredWordDocumentLoader
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.text_splitter import CharacterTextSplitter
from langchain_openai import OpenAI
import os
import tempfile

def process_document(doc_sources, source_type):
    documents = []
    
    if source_type == "PDF":
        for doc in doc_sources:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
                tmp_file.write(doc.read())
                loader = PyPDFLoader(tmp_file.name)
                documents.extend(loader.load())
    
    elif source_type == "DOCX":
        for doc in doc_sources:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".docx") as tmp_file:
                tmp_file.write(doc.read())
                loader = UnstructuredWordDocumentLoader(tmp_file.name)
                documents.extend(loader.load())
    
    else:  # Text file
        for doc in doc_sources:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".txt", mode="w+") as tmp_file:
                content = doc.getvalue().decode("utf-8")
                tmp_file.write(content)
                loader = TextLoader(tmp_file.name)
                documents.extend(loader.load())
    
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    texts = text_splitter.split_documents(documents)
    
    embeddings = OpenAIEmbeddings()
    db = Chroma.from_documents(texts, embeddings)
    
    return db

def get_conversation_chain(vector_store):
    llm = OpenAI()
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vector_store.as_retriever(),
    )
    return conversation_chain

st.set_page_config(page_title="Interactive Document Q&A", layout="wide")

st.title("Talk to your data")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "api_key" not in st.session_state:
    st.session_state.api_key = ""

# Sidebar for API key and source selection
with st.sidebar:
    st.header("NOVELTY TECHNOLOGY")
    api_key = st.text_input("Enter your OpenAI API key:", type="password", value=st.session_state.api_key)
    if api_key:
        st.session_state.api_key = api_key
        os.environ["OPENAI_API_KEY"] = api_key

# Main content area
if st.session_state.api_key:
    col1, col2 = st.columns([2, 1])

    with col1:
        file_type = st.radio("Select file type:", ("PDF", "DOCX"))
        uploaded_files = st.file_uploader(f"Choose {file_type} files", type="pdf" if file_type == "PDF" else "docx", accept_multiple_files=True)
        if uploaded_files:
            with st.spinner("Processing document(s)..."):
                vector_store = process_document(uploaded_files, file_type)
                conversation_chain = get_conversation_chain(vector_store)
            st.success("Document(s) processed successfully!")

        user_question = st.text_input("Ask a question about the document:")
        
        if user_question:
            with st.spinner("Generating answer..."):
                if 'conversation_chain' in locals():
                    response = conversation_chain({"question": user_question, "chat_history": st.session_state.chat_history})
                    answer = response["answer"]
                else:
                    answer = "Please process a document before asking questions."

            st.write("Answer:", answer)
            st.session_state.chat_history.append((user_question, answer))

    with col2:
        st.subheader("Chat History")
        for i, (question, answer) in enumerate(reversed(st.session_state.chat_history)):
            with st.expander(f"Q{len(st.session_state.chat_history)-i}: {question[:50]}..."):
                st.write(f"**Question:** {question}")
                st.write(f"**Answer:** {answer}")

    # Add a button to clear chat history
    if st.button("Clear Chat History"):
        st.session_state.chat_history = []
        st.rerun()
else:
    st.warning("Please enter your OpenAI API key in the sidebar to proceed..")
