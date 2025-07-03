from llm import llm
from graph import graph
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.prompts import PromptTemplate
from langchain.schema import StrOutputParser
from langchain.tools import Tool
from langchain_neo4j import Neo4jChatMessageHistory
from langchain.agents import AgentExecutor, create_react_agent
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain import hub
from utils import get_session_id
from tools.vector import get_abstracts
from tools.cypher import cypher_qa


chat_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a medical expert providing information about pubmed article abstracts."),
        ("human", "{input}"),
    ]
)

pubmed_chat = chat_prompt | llm | StrOutputParser()

# Create a set of tools
from langchain.tools import Tool

tools = [#list of tools
    Tool.from_function(
        name="General Chat",
        description="For general scientific chat not covered by other tools",
        func=pubmed_chat.invoke,
    ), 
     Tool.from_function(
        name="Abstracts",  
        description="For when you need to find information within pubmed abstracts",
        func=get_abstracts, 
    ),
    Tool.from_function(
        name="Abstract Information Graph Enhanced",
        description="Provide information about medical and scientific questions using Cypher",
        func = cypher_qa
    )
]
# Create chat history callback: creating memory
from langchain_neo4j import Neo4jChatMessageHistory

def get_memory(session_id):
    return Neo4jChatMessageHistory(session_id=session_id, graph=graph)

# Create the agent
from langchain.agents import AgentExecutor, create_react_agent
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain import hub

agent_prompt = PromptTemplate.from_template("""
 You are a scientific, medical expert providing information and sources from pubmed article abstracts.
You will be provided with a set of tools to answer questions.
                                            
You are a helpful medical assistant. You must always output valid ReAct format steps. "
"Never just say 'I don't know'. If you do not know the answer, output: "
"Thought: I do not know the answer.\nFinal Answer: I do not know."
                                            
Use the tools to answer the question.
Do not answer any questions that do not relate to medical or scienftic knowledge.
Do not answer any questions using your pre-trained knowledge, only use the information provided in the context.
 
You should provide authors and PMIDs when answering a question. 
Use the Abstract Information Graph Enhanced tool to find out PMIDs and Authors.
Use the Abstracts tool to find information within articles. 
                                        
When you have used a cypher query, ALWAYS return the pmid to the human
                                            
TOOLS: 
{tools}
                                            
To use a tool, please use the following format:

```
Thought: Do I need to use a tool? Yes
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
```

When you have a response to say to the Human, or if you do not need to use a tool, you MUST use the format:

```
Thought: Do I need to use a tool? No
Final Answer: [your response here]

```

Begin!

Previous conversation history:
{chat_history}

New input: {input}
{agent_scratchpad}
""")


agent = create_react_agent(llm, tools, agent_prompt) # reasoning and acting agent type
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,
    handle_parsing_errors=True
    )

chat_agent = RunnableWithMessageHistory( # handiliing chat history
    agent_executor,
    get_memory,
    input_messages_key="input",
    history_messages_key="chat_history",
)
# Create a handler to call the agent

from utils import get_session_id

def generate_response(user_input):
    """
    Create a handler that calls the Conversational agent
    and returns a response to be rendered in the UI
    """

    response = chat_agent.invoke(
        {"input": user_input},
        {"configurable": {"session_id": get_session_id()}},)

    return response['output']
