import os
import streamlit as st
from llama_index import GPTVectorStoreIndex, Document, SimpleDirectoryReader #GPTSimpleVectorIndex

st.title("DocuSearch GPT")
st.write("A document indexing and querying application that helps users to quickly search through their collections of documents, articles, research papers, and reports. DocuSearch uses OpenAI GPT model to extract vectors representing each document, enabling users to search for relevant information within their collection.")

api = st.text_input('Enter Your OpenAI API')

if api:
     os.environ['OPENAI_API_KEY'] = api
else:
     st.error("Please Enter Your OpenAI API Key")

def save_file(file, folder):
    if folder not in os.listdir():
            os.makedirs(folder)
    with open(os.path.join(folder, file.name), "wb") as f:
        f.write(file.getvalue())

uploaded_files = st.file_uploader("Choose .txt files to upload", accept_multiple_files=True, type="txt")

if uploaded_files:
    for uploaded_file in uploaded_files:
        save_file(uploaded_file, "index")
        st.info(f"{uploaded_file.name} saved to index folder.")

index = None  # Define index outside of the if block

button1 = st.button('Start Indexing Document')
if st.session_state.get('button') != True:
        st.session_state['button'] = button1 # Saved the state

if st.session_state['button'] == True:
    documents = SimpleDirectoryReader('index').load_data()
    index = GPTVectorStoreIndex.from_documents(documents)
    #st.info(index.query("what is mobile number of heera lal"))
    st.success("Indexing Done!")
    query_ques = st.text_input("Enter What you want To Ask?")
    if st.button("Get Answer"):
        #response = index.query(query_ques)
          query_engine = index.as_query_engine()
         response = query_engine.query(query_ques)
        st.write(response)
