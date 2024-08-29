# MultiDocs_Bot

## **Introduction**

This project demonstrates how to build an interactive document question-answering (Q&A) application using RAG, LangChain, OpenAI and Streamlit. The application allows users to upload PDF or DOCX documents, process them, and then ask questions about the content. The answers are generated using OpenAI's language model and the LangChain library, which maintains conversational context.

## **Key Features**

1. **Streamlit**: Streamlit is used to create the web interface for the application, allowing users to easily upload documents, enter questions, and view answers.
2. **LangChain**: LangChain is a library that helps manage the conversation history and structure the responses from OpenAI's language model.
3. **OpenAI**: OpenAI's(API Key) GPT language model is used to generate the answers to the user's questions based on the uploaded documents.
4. **Conversational Memory**: The application maintains conversational memory, meaning it can reference past exchanges in its responses, leading to a more coherent and engaging user experience.

## **How It Works**

1. **Users enter their OpenAI API key** in the sidebar to authenticate with the OpenAI API.
2. **Users select the file type (PDF or DOCX)** and upload one or more documents.
3. **The uploaded documents are processed** using the specified file loader (PyPDFLoader for PDF, UnstructuredWordDocumentLoader for DOCX) and split into smaller chunks using CharacterTextSplitter.
4. **The document chunks are embedded** using OpenAIEmbeddings and stored in a Chroma vector store.
5. **A ConversationalRetrievalChain is created** using the vector store and OpenAI's language model.
6. **Users can then enter questions** about the uploaded documents in the text input field.
7. **The application generates answers** using the ConversationalRetrievalChain, which retrieves relevant information from the vector store and generates a response using the language model.
8. **The questions and answers are stored** in the session state and displayed in the chat history section.
9. **Users can clear the chat history** using the "Clear Chat History" button.

## **Conclusion**

This  chatbot combines the power of RAG, LangChain, OpenAI and Streamlit to create an interactive document Q&A application. It demonstrates how to process and store documents, generate answers using language models, and maintain conversational context. The application can be easily customized and extended to suit various use cases, making it a valuable tool for both technical and non-technical staff.
