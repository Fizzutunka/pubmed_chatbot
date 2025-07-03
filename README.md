# pubmed_chatbot
A streamlit chatbot with RAG suitable for querying PubMed abstracts. 


# TO DO

LINE 76 data_import.py : Provide a pathname to your local xml file. 

Suitable xml files can be unzipped from https://ftp.ncbi.nlm.nih.gov/pubmed/baseline/ 


Create a ./streamlit file with a .secrets/toml containing:

  GOOGLE_API_KEY = ""
  GOOGLE_MODEL = "" e.g gemini-2.5-flash-lite-preview-06-17

/or 

  OPENAI_API_KEY=""
  OPENAI_MODEL=""
  
/and 
  NEO4J_URI = ""
  NEO4J_USERNAME = ""
  NEO4J_PASSWORD = ""


Create a .env file containing 

  NEO4J_URI = ""
  NEO4J_USERNAME = ""
  NEO4J_PASSWORD = ""
