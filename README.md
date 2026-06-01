Tracing LLM calls (Projects, Traces, Runs) in LangSmith

Project is one LLM pipeline, eg. INPUT -> LLM -> OutputParser -> Output

Trace is a single execution of the above pipeline.

Runs is every single component in the pipeline, so here, LLM, OutputParser, and Output.

1. 1_simple_llm_call.py

Tracing a simple Project ewith Chain: prompt → model → parser and it's LLM call with multiple executions (traces) and runs in that.

2. 2_sequential_chain.py

Tracing a complex pipeline with multiple models and parsers, along with adding custom trace name (instead of the defaul Runnable Sequence) and adding custom tags and metadata.

3. 3_rag_v1.py

When a RAG app fails, there are almost always 2 reasons for it:

i. Retriever errors: wrong/irrelevant docs retrieved
ii. Generator errors: model hallucinates or misuses context

And in production systems, it is often unclear where the failure happened. Was the retriever bad or did the LLM ignore docs.

With LangSmith, following is recorded:

i. User query
ii. Retrieved documents
iii. LLM Prompt (with inserted docs)
iv. LLM response

So we can check every run in a trace to see where exactly the issue was.