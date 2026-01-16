"""Prompt templates for the research agent."""

from langchain_core.prompts import PromptTemplate

# Query Analysis Prompt
QUERY_ANALYSIS_PROMPT = PromptTemplate(
    input_variables=["query"],
    template="""Analyze the following research query and determine the best approach to answer it.

Query: {query}

Please answer the following:
1. Does this query require searching a local knowledge base? (yes/no)
2. Does this query require current information from the web? (yes/no)
3. If the query is complex, break it down into 2-3 sub-questions.

Provide your analysis in the following format:
LOCAL_SEARCH: [yes/no]
WEB_SEARCH: [yes/no]
SUB_QUESTIONS:
- [sub-question 1]
- [sub-question 2]
- [sub-question 3]

Keep sub-questions focused and relevant to the main query."""
)

# Relevance Check Prompt
RELEVANCE_CHECK_PROMPT = PromptTemplate(
    input_variables=["query", "documents"],
    template="""Evaluate if the retrieved documents sufficiently answer the research query.

Query: {query}

Retrieved Documents:
{documents}

Rate the relevance on a scale of 0-10:
- 0-3: Documents are not relevant or insufficient
- 4-6: Documents are somewhat relevant but missing key information
- 7-10: Documents are highly relevant and sufficient to answer the query

Provide your evaluation in the following format:
RELEVANCE_SCORE: [0-10]
REASONING: [brief explanation of the score]
MISSING_INFO: [what information is missing, if any]"""
)

# Synthesis Prompt
SYNTHESIS_PROMPT = PromptTemplate(
    input_variables=["query", "documents"],
    template="""Synthesize a comprehensive answer to the research query based on the provided documents.

Query: {query}

Source Documents:
{documents}

Please provide:
1. A clear, comprehensive answer to the query
2. Cite sources by referencing document metadata (e.g., [Source: filename.pdf])
3. Acknowledge any gaps or limitations in the available information
4. Organize the answer in a structured format with sections if appropriate

Your answer should be well-researched, accurate, and directly address the query."""
)

# Research Planning Prompt
RESEARCH_PLANNING_PROMPT = PromptTemplate(
    input_variables=["query"],
    template="""Create a research plan to answer the following query.

Query: {query}

Break down the query into specific research steps:
1. Identify the main topics and concepts
2. List 2-4 focused sub-questions that need to be answered
3. Suggest what type of information sources would be most relevant

Provide your plan in the following format:
MAIN_TOPICS: [list main topics]
SUB_QUESTIONS:
- [sub-question 1]
- [sub-question 2]
- [sub-question 3]
SUGGESTED_SOURCES: [local documents, web search, or both]"""
)

# Web Search Query Generation Prompt
WEB_SEARCH_QUERY_PROMPT = PromptTemplate(
    input_variables=["query", "missing_info"],
    template="""Generate effective web search queries to find missing information.

Original Query: {query}
Missing Information: {missing_info}

Generate 2-3 specific search queries that would help find the missing information.
Make the queries clear, focused, and optimized for search engines.

Provide your queries in the following format:
SEARCH_QUERIES:
- [query 1]
- [query 2]
- [query 3]"""
)


def format_documents_for_prompt(documents) -> str:
    """
    Format documents for inclusion in prompts.

    Args:
        documents: List of Document objects

    Returns:
        Formatted string of documents
    """
    if not documents:
        return "No documents available."

    formatted = []
    for i, doc in enumerate(documents, 1):
        source = doc.metadata.get("source", "Unknown")
        content = doc.page_content[:500]  # Limit content length
        formatted.append(f"Document {i} [Source: {source}]:\n{content}\n")

    return "\n".join(formatted)
