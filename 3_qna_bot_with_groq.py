from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain.agents import create_agent
from langchain_community.utilities import GoogleSerperAPIWrapper
from langgraph.checkpoint.memory import InMemorySaver  
import streamlit as st
load_dotenv()

llm=ChatGroq(model="openai/gpt-oss-120b",streaming=True)
search=GoogleSerperAPIWrapper()

if "memory" not in st.session_state:    
    st.session_state.memory=InMemorySaver()
    st.session_state.history=[]
agent=create_agent(model=llm,
                   tools=[search.run],
                   system_prompt="You are a agent who can search the internet for any new information.",
                   checkpointer=st.session_state.memory)

st.subheader("QuickAnswer-A fast Chatbot")
for message in st.session_state.history:
    role=message["role"]
    content=message["content"]
    st.chat_message(role).markdown(content)
query=st.chat_input("Ask anything ")
if query:
    st.chat_message("user").markdown(query)
    st.session_state.history.append({"role":"user","content":query})
    thread_config = {"configurable": {"thread_id": "1"}}
    response=agent.stream({"messages":st.session_state.history},thread_config,stream_mode="messages")
    ai_container=st.chat_message("ai")
    with ai_container:
        space=st.empty()
        message=""
        for chunk in response:
            message=message+chunk[0].content
            space.markdown(message)
    st.session_state.history.append({"role":"ai","content":message})
