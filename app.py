import os
import streamlit as st
from llama_index import GPTVectorStoreIndex, Document, SimpleDirectoryReader
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
from requests_oauthlib import OAuth1Session

st.title("DocuQuery: Instant Answers from Documents with AI")
st.write("<p>Introducing DocuQuery, your key to unlocking a world of instant knowledge within your documents. With the power of AI, this cutting-edge application revolutionizes the way you access information. No more tedious searches or manual scanning – simply upload your document, ask a question, and let DocuQuery deliver precise and immediate answers. Whether you're a student, researcher, or professional, DocuQuery empowers you to delve deeper, work smarter, and make informed decisions effortlessly. Experience the future of document search and discovery at your fingertips with DocuQuery.</p>",unsafe_allow_html=True)

with open("config.yaml") as file:
    config = yaml.load(file, Loader=SafeLoader)
authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)
name, authentication_status, username = authenticator.login('Login', 'main')

if authentication_status:
    authenticator.logout('Logout', 'main', key='unique_key')
    st.write(f'Welcome *{name}*')

    def save_file(file, folder):
        if folder not in os.listdir():
                os.makedirs(folder)
        with open(os.path.join(folder, file.name), "wb") as f:
            f.write(file.getvalue())
            
    api = st.text_input('Enter Your credentials',type='password')
    if api:
         os.environ['OPENAI_API_KEY'] = api
    else:
         st.error("Please Enter Your credentials")

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
        st.success("Indexing Done!")
        query_ques = st.text_input("Enter What you want To Ask?")
        if st.button("Get Answer"):
            query_engine = index.as_query_engine()
            response = query_engine.query(query_ques)
            st.write(response)

elif authentication_status is False:
    st.error('Username/password is incorrect')
