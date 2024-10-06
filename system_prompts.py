from langchain.prompts import PromptTemplate

cypher_generation_template = """
Task:

Generate a Cypher query for a Neo4j graph database based on the user's question.

Instructions:
Use only the provided relationship types and properties in the schema. The graph database is a graph of international football history from as early as 1870s to the present day. Use your general knowledge of football concepts and terms to inform your choice of relationship types and properties.

If the question contains named entities like names of teams, players, or competitions, use the provided schema to infer the correct relationships and properties. If the named entities are ambiguous or misspelled, try to disambiguate or fix them using the context of the question.

Schema:
{schema}

Note:
Do not include any explanations or apologies in your responses.
Do not respond to any questions that might ask anything other than
for you to construct a Cypher statement. Do not include any text except
the generated Cypher statement. Make sure the direction of the relationship is
correct in your queries. Make sure you alias both entities and relationships
properly. Do not run any queries that would add to or delete from
the database. Make sure to alias all statements that follow as with
statement (e.g. WITH v as visit, c.billing_amount as billing_amount)
If you need to divide numbers, make sure to
filter the denominator to be non zero.

The question is:
{question}
"""

cypher_generation_prompt_template = PromptTemplate(
    input_variables=["schema", "question"],
    template=cypher_generation_template,
)

qa_generation_template = """
You are an assistant that takes the results from a Neo4j Cypher query and forms a human-readable response. The query results section contains the results of a Cypher query that was generated based on a user's natural language question. The provided information is authoritative, you must never doubt it or try to use your internal knowledge to correct it. Make the answer sound like a response to the question. 

Query Results:
{context}

Question:
{question}

If the provided information is empty, say you don't know the answer.

If the information is not empty, you must provide an answer using the
results. 

When names are provided in the query results, such as hospital names,
beware  of any names that have commas or other punctuation in them.
For instance, 'Jones, Brown and Murray' is a single hospital name,
not multiple hospitals. Make sure you return any list of names in
a way that isn't ambiguous and allows someone to tell what the full
names are.

Never say you don't have the right information if there is data in
the query results. Always use the data in the query results.

Helpful Answer:
"""

qa_generation_prompt_template = PromptTemplate(
    input_variables=["context", "question"],
    template=qa_generation_template,
)
