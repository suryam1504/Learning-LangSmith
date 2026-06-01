from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
import os
os.environ['LANGCHAIN_PROJECT'] = 'Sequential LLM App' # if we wont set this, this file would be traced in langsmith in the same project as 1_simple_llm_call.py which is 'learning-langsmith', by default in .env. But ideally, different projects/files should be traced in diff projets, so instead of changing .env every time, we can set it here in code itself

load_dotenv()

prompt1 = PromptTemplate(
    template='Generate a detailed report on {topic}',
    input_variables=['topic']
)

prompt2 = PromptTemplate(
    template='Generate a 5 pointer summary from the following text \n {text}',
    input_variables=['text']
)

model1 = ChatOpenAI(model='gpt-4o-mini', temperature=0.7)

model2 = ChatOpenAI(model='gpt-4o', temperature=0.5)

parser = StrOutputParser()

chain = prompt1 | model1 | parser | prompt2 | model2 | parser

# we can define custom tags and metadata for this chain which will be visible in langsmith tracing UI, this is optional but good to have for better orgnization and filtering in langsmith
config = {
    'run_name': 'Report Generation and Summarization Chain', # to set a custom name in langsmith instead of the default RunnableSequence
    'tags': ['llm app', 'report generation', 'summarization'],
    'metadata': {'model1': 'gpt-4o-mini', 'model2': 'gpt-4o', 'model1_temperature': 0.7, 'model2_temperature': 0.5, 'parser': 'StrOutputParser'}
}

result = chain.invoke({'topic': 'Unemployment in India'}, config=config)

print(result)
