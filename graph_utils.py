import streamlit as st
from langchain.chains import GraphCypherQAChain
from langchain_community.graphs import Neo4jGraph
from langchain_openai import ChatOpenAI


@st.cache_resource(show_spinner=False)
def init_resources(api_key):
    graph = Neo4jGraph(
        url=st.secrets["NEO4J_URI"],
        username=st.secrets["NEO4J_USER"],
        password=st.secrets["NEO4J_PASSWORD"],
        enhanced_schema=True,
    )
    graph.refresh_schema()

    chain = GraphCypherQAChain.from_llm(
        ChatOpenAI(api_key=api_key, model="gpt-4", temperature=0),
        graph=graph,
        verbose=True,
        show_intermediate_steps=True,
        allow_dangerous_requests=True,
    )
    return graph, chain


@st.cache_data(ttl=3600, show_spinner=False)  # Cache for 1 hour
def query_graph(chain, query):
    try:
        result = chain.invoke({"query": query})["result"]
        return result
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        return "I'm sorry, I encountered an error while processing your request."
