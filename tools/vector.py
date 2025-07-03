import streamlit as st
from llm import llm, embeddings
from graph import graph
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
from langchain_neo4j import Neo4jVector

# Create the embedding model

abstract_vector = Neo4jVector.from_existing_index(
    embeddings,
    graph=graph,
    index_name="vector", # The name of the index to use
    embedding_node_property="abstract_vectors",# The property containing the embedding vector
    text_node_property="abstract",# The property containing the text to embed
)
# Create the retriever
retriever = abstract_vector.as_retriever()
# Create the prompt
instructions = (
    """
    "You are a helpful scientific assistant. "
    "Use the given context (PubMed abstracts) to answer the question. "
    "If you don't know the answer from the context, say 'I don't know'." 
    "\n\nContext: {context}"
    """
)

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", instructions),
        ("human", "{input}"),
    ]
)
# Create the chain 
question_answer_chain = create_stuff_documents_chain(llm, prompt)
abstract_retriever = create_retrieval_chain(
    retriever, 
    question_answer_chain
)
# Create a function to call the chain
def get_abstracts(input):
    return abstract_retriever.invoke({"input": input})