# LangSmith

LangSmith is a unified observability and evaluation platform that helps developers and teams debug, test, and monitor AI application performance — specifically by tracing LLM calls across Projects, Traces, and Runs.

**Observability** is the ability to understand a system's internal state by examining its external outputs such as logs, metrics, and traces. It allows us to diagnose issues, understand performance, and improve reliability.

LangSmith traces:

- Inputs and outputs
- All intermediate steps
- Latency
- Token usage
- Cost
- Errors
- Tags
- Metadata
- Feedback

### Key Definitions

- **Project** — one LLM pipeline, e.g. `INPUT → Prompt → LLM → OutputParser → Output`
- **Trace** — a single execution of the above pipeline
- **Run** — every individual component within a trace (e.g. Prompt, LLM, OutputParser, Output)

---

## Files

### 1. `1_simple_llm_call.py`

Traces a simple project with a chain: `prompt → model → parser`, including its LLM call with multiple executions (traces) and runs.

### 2. `2_sequential_chain.py`

Traces a complex pipeline with multiple models and parsers. Also demonstrates adding a custom trace name (instead of the default `RunnableSequence`) and adding custom tags and metadata.

---

### Tracing in RAG

When a RAG app fails, there are almost always two reasons:

1. **Retriever errors** — wrong or irrelevant documents retrieved
2. **Generator errors** — the model hallucinates or misuses the context

In production systems, it is often unclear where the failure occurred: was the retriever bad, or did the LLM ignore the retrieved documents?

With LangSmith, the following is recorded for every trace:

1. User query
2. Retrieved documents
3. LLM prompt (with inserted documents)
4. LLM response

This makes it possible to inspect every run in a trace and pinpoint exactly where the issue occurred.

---

### 3. `3_rag_v1.py`

Traces a simple RAG application.

**Problems:**

1. Only the invokable portion of the pipeline is traced in LangSmith — specifically `parallel | prompt | llm | StrOutputParser()`. Steps like PDF loading, chunking, and embedding are not captured, so there is no visibility into how long they took or what they produced.

2. There is a logical inefficiency: every time the script runs, it reloads, re-chunks, and re-embeds the PDF. Ideally, these results should be saved on the first run and reused in subsequent runs.

### 4. `3_rag_v2.py`

Solves the first problem from above by wrapping non-invokable functions with the `@traceable` decorator so they are captured as traced runs in LangSmith.

**Remaining problem:**

LangSmith shows two separate traces — one for `setup_pipeline` (with child spans for `load_pdf`, `split_documents`, and `build_vectorstore`) and another for `pdf_rag_query` (with child spans for the retriever and LLM calls). This makes the execution look like two separate pipelines, when ideally it should appear as a single trace with both setup and query steps nested inside.

### 5. `3_rag_v3.py`

Introduces a top-level `pdf_rag_full_run` function so that both the setup and the LLM query appear as a single trace in LangSmith, with all child spans nested inside. Also demonstrates how to add custom tags and metadata to `@traceable` decorator functions.

### 6. `3_rag_v4.py`

Solves the logical inefficiency from `3_rag_v1.py` by saving the vectorstore to disk after it is built for the first time, and loading it from disk on subsequent runs if it already exists. Uses content-aware cache keying (SHA-256 hash of the PDF, chunk size, chunk overlap, and embedding model) so the index is automatically rebuilt if any of those parameters change.

### 7. `4_agent.py`

Traces a simple ReAct agent, capturing its internal reasoning, actions, and tool calls.

### 8. `5_langgraph.py`

In LangGraph:

- Every graph execution is a trace.
- Each node (e.g. retriever, LLM, tool call, subgraph) is a run inside the trace.
- The path taken through the graph is visualized, e.g. `START → Retriever → Reranker → LLM Answer → END`.
- If a workflow branches (conditional, parallel, or subgraph), LangSmith captures which path was taken and executed.

---

## Other LangSmith Features

- **Monitoring and Alerting** — Aggregates key metrics across many traces (latency, token usage, cost, error rates, success rates, etc.) to track the overall health of an LLM system. Alerts can be configured to trigger when metrics fall outside acceptable ranges (e.g. a spike in cost or token usage), enabling fast debugging.

- **Evaluation** — Since LLMs are non-deterministic, evaluation in LangSmith provides a systematic way to measure output quality. Tests can be run against gold-standard datasets using custom metrics such as faithfulness, relevance, or completeness. Supported approaches include automated scoring with LLM-as-a-judge, semantic similarity checks, and custom Python evaluators. Evaluations can be run offline (batch tests before deployment) or online (continuous checks on live traffic).

  LLM behavior can be unpredictable — a small change in prompts, models, or retrieval logic may improve some cases while breaking others. Evaluation provides an objective, repeatable way to track performance over time, ensuring that new versions are genuinely better and preventing regressions.

  **Example** — for a RAG chatbot, you might evaluate:
  - **Faithfulness** → Are answers grounded in the retrieved documents?
  - **Relevance** → Does the response actually address the user's question?

  By running the same dataset across GPT-4, Claude, and LLaMA, you can directly compare which model or pipeline configuration performs best.

- **Prompt Experimentation** — Enables systematic testing and comparison of different prompt versions. A/B tests can be run across prompts on the same dataset, with performance tracked against evaluation metrics and results stored over time. This provides a clear history of which prompt variations worked best and under what conditions, and can also be used to compare behavior across different models.

- **Dataset Creation and Annotation** — Build and label datasets for evaluation and fine-tuning directly within LangSmith.

- **User Feedback Integration** — Collect thumbs up/down ratings or structured feedback from users in production and associate it with specific traces.

- **Collaboration** — Share a link to any trace with a team member so they can inspect and analyze it directly.
