import streamlit as st
from langchain.chains import GraphCypherQAChain
from langchain_community.graphs import Neo4jGraph
from langchain_openai import ChatOpenAI
from system_prompts import (
    cypher_generation_prompt_template,
    qa_generation_prompt_template,
)


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
        cypher_llm=ChatOpenAI(api_key=api_key, model="gpt-4o", temperature=0),
        qa_llm=ChatOpenAI(api_key=api_key, model="gpt-4o", temperature=0),
        graph=graph,
        verbose=True,
        show_intermediate_steps=True,
        allow_dangerous_requests=True,
        qa_prompt=qa_generation_prompt_template,
        cypher_prompt=cypher_generation_prompt_template,
        validate_cypher=True,
    )
    return graph, chain


def query_graph(chain, query):
    result = chain.invoke({"query": query})["result"]
    return result
