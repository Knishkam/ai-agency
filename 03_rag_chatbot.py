import os
import streamlit as st
from groq import Groq
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
client = Groq(api_key=os.environ.get("Groq_API_Key"))
st.title("AI Document Assistant")
st.write(("Upload a PDF document and ask questions about its content!"))
uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")
if uploaded_file:
    with open("temp.pdf", "wb") as f:
        f.write(uploaded_file.read())
        loader = PyPDFLoader("temp.pdf")
        documents = loader.load()
        splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
        chunks = splitter.split_documents(documents)
        embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
        vectorstore = Chroma.from_documents(chunks, embeddings)
        st.success("Document processed successfully! f{len(chunks)} chunks created.")
        question = st.text_input("Ask a question about the document:")
        if question:
            docs = vectorstore.similarity_search(question, k=3)
            context = "\n".join([doc.page_content for doc in docs])
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {
                        "role": "system",
                        "content": f"Sirf is context se jabab do:\n{context}"
                    },
                    {
                        "role": "user",
                        "content": question
                    }
                ]
            )
            st.write(f"Answer:")
            st.write(response.choices[0].message.content)