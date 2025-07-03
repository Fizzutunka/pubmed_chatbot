import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_google_genai import GoogleGenerativeAIEmbeddings
# from neo4j_graphrag.embeddings.openai import OpenAIEmbeddings
# from neo4j_graphrag.llm import OpenAILLM

# create the llm
llm = ChatGoogleGenerativeAI(
    google_api_key=st.secrets["GOOGLE_API_KEY"],
    model=st.secrets["GOOGLE_MODEL"],
)

# Create the Embedding model : Google
embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

# Create the Embedding model : OPENAI
# embeddings = OpenAIEmbeddings(model="text-embedding-ada-002")

