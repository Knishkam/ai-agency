import os
from dotenv import load_dotenv
load_dotenv()
import streamlit as st
from groq import Groq
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

st.title("📄 AI Document Assistant")
st.write("Apna PDF upload karo aur sawaal pucho!")

uploaded_file = st.file_uploader("PDF Upload Karo", type="pdf")

if uploaded_file:
    with open("temp.pdf", "wb") as f:
        f.write(uploaded_file.read())
    
    loader = PyPDFLoader("temp.pdf")
    pages = loader.load()
    
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )
    chunks = splitter.split_documents(pages)
    
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )
    vectorstore = Chroma.from_documents(chunks, embeddings)
    
    st.success(f"✅ PDF load hua! {len(chunks)} chunks bane!")
    
    question = st.text_input("Sawaal Pucho:")
    
    if question:
        docs = vectorstore.similarity_search(question, k=3)
        context = "\n".join([doc.page_content for doc in docs])
        
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": f"Sirf is context se jawab do:\n{context}"
                },
                {
                    "role": "user",
                    "content": question
                }
            ]
        )
        
        st.write("### 🤖 AI Ka Jawab:")
        st.write(response.choices[0].message.content)