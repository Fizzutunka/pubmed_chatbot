import streamlit as st
from llm import llm
from graph import graph
from langchain_neo4j import GraphCypherQAChain
from langchain.prompts.prompt import PromptTemplate

# fine tuning cypher template with few-shot

cypher_template = """Task:Generate Cypher statement to query a graph database.
Instructions:
Use only the provided relationship types and properties in the schema.
Do not use any other relationship types or properties that are not provided.

Schema:
{schema}
Examples:
1. Question: Get authors of an article?
   Cypher: MATCH (a:Article)<-[:WROTE]-(auth:Author) WHERE a.pmid = "your_pmid_here" RETURN collect(auth.name) AS authors
2. Question: Get PMID of an article?
   Cypher: MATCH (a:Article) WHERE a.title = "Your Article Title Here" RETURN a.pmid AS pmid
3. Question: Whats is the published date of an article? 
   Cypher: MATCH (a:Article) WHERE a.pmid = ""your_pmid_here" RETURN a.pub_date as date

Note: Do not include any explanations or apologies in your responses.
Do not respond to any questions that might ask anything else than for you to construct a Cypher statement.
Do not include any text except the generated Cypher statement.

if "```" in generated_cypher:
    generated_cypher = generated_cypher.replace("```", "").strip()


The question is:
{question}
"""

cypher_prompt = PromptTemplate.from_template(cypher_template)

# Create the Cypher QA chain
cypher_qa = GraphCypherQAChain.from_llm(
    llm,
    graph=graph,
    verbose=True,
    cypher_prompt=cypher_prompt,
    allow_dangerous_requests=True
)

