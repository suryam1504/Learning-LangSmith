# LangSmith

Helps with uified Observability and evaluation platform where we/teams can debug, test, and monitor AI app performance.

Essentially, tracing LLM calls (Projects, Traces, Runs) in LangSmith

Helps in Observability, which is the ability to understand a system's internal state by examining its external outputs like logs, metrics, and traces. It allows us to diagnose issues, understand performance, and improve reliability. 

LangSmith traces:

- Inputs and Outputs
- All intermediate steps
- Latency
- Token Usage
- Cost
- Error
- Tags
- Metadata
- Feeedback

Some LangSmith definitions:

- Project is one LLM pipeline, eg. INPUT -> Prompt -> LLM -> OutputParser -> Output

- Trace is a single execution of the above pipeline.

- Runs is every single component in the pipeline, so here, Prompt, LLM, OutputParser, and Output.

1. 1_simple_llm_call.py

Tracing a simple Project ewith Chain: prompt → model → parser and it's LLM call with multiple executions (traces) and runs in that.

2. 2_sequential_chain.py

Tracing a complex pipeline with multiple models and parsers, along with adding custom trace name (instead of the defaul Runnable Sequence) and adding custom tags and metadata.

Tracing in RAG

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

3. 3_rag_v1.py

Tracing a simple RAG application.

Problems:

i. If we look in LangSmith, we notice that technically, our whole RAG sysstem is not getting traced, only the parts where invoke happens, so essentially these guys - parallel | prompt | llm | StrOutputParser(). There is no tracing of what pdf was loaded, how much time that took, how the pdf was chunked and its time, how chunks were embedded, how much time retriever took to get relevant chunks, etc.

ii. Slight logical issue in code which results in latency issues - if we run this file again, it will again take a lot of time bcoz pdf gets loaded chunked embedded again, but ideally in the first run itself it should have had saved stuff somewhere so next run we have these things ready and we can just ask question. 

4. 3_rag_v2.py

Solving the first problem from above by importing traceable and make functions of things which aren't technically invokable, and whichever functions we want to get traced, wrap them in traceable decorator.

Problems:

In LangSmith, we see that 2 traces are created - one for setup_pipeline which has child spans for load_pdf, split_documents, build_vectorstore, and another trace for pdf_rag_query which has child spans for retriever and llm calls. We can see the time taken by each step, the inputs/outputs, etc.

Great, but formation of 2 traces in LangSmith makes it look like these are 2 separate executions, ideally we would have liked there to be only 1 trace, and inside we should have had setup_pipeline and LLM calls.

5. 3_rag_v3.py

Making a top level pdf_rag_full_run, so just one run which has setup and llm calls inside, and how to add custom tags and metadata in decorator functions to be traced by LangSmith

6. 3_rag_v4.py

Solving the logical issue of setup steps getting repeated every time we ask a question, we solve that by saving the vectorstore to disk after creating it for the first time, and loading from disk in subsequent runs if it exists.

7. 4_agent.py

Tracing a simple ReAct agent and hence it's internal reasoning and actions and tool calling.

8. 5_langgraph.py

In LangGraph,

- Every graph execution is a trace.
- Each node (eg. retriever, LLM, tool call, subgraph) is a run inside the trace.
- We can visualize the path taken: eg. START -> Retriever -> Reranker -> LLM Answer -> END
- If a workflow branches (conditional/parallel/subgraph), LangSmith captures which path was taken and executed.


