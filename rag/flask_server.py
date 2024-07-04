import os
from flask import Flask, request
from markupsafe import escape
from llama_index.core import Settings
from llama_index.llms.openai import OpenAI
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.llms.ollama import Ollama
from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core import SimpleDirectoryReader, VectorStoreIndex
from llama_index.core import StorageContext, load_index_from_storage
from llama_index.core.tools import QueryEngineTool
from llama_index.core.query_engine.router_query_engine import RouterQueryEngine
from llama_index.core.selectors import LLMSingleSelector

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


# Settings.llm = OpenAI(model="gpt-3.5-turbo", api_key=os.getenv('OPENAI_API_KEY'))
# Settings.embed_model = OpenAIEmbedding(model="text-embedding-ada-002")
# input_files = [
#     "idpp.pdf", "metagpt.pdf", "state_of_the_union.txt", "Federal Tax Return 2021.pdf", "Financial Assessment.docx",
#     "IELTS Result - March 2023.pdf", "Shashank Verma - Resume.pdf", 'Shashank Verma - Resume (2024).pdf', 'LLM Pointers.pdf',
#     'Multi-class classification via Transfer Learning for classifying dog breeds from images.pdf',
#     'Incorporating adaptive feedback capability to Interactive Videos tutor in Project Ivy.pdf', 'Spring 2024 Reflection Report - Shashank.pdf',
#     'Shashank - Medical Log.pdf', 'Pranjali - Medical Log.pdf', 'Shashank - 2023-06-16 Lab Results.pdf', 'Pranjali - 2023-06-16 Lab Results.pdf',
#     'Trippy Trip.pdf']
# input_files = ["../data/" + item for item in input_files]

# file_summaries = [
#     "Useful for retrieving specific context from the iDPP paper which is about predicting ALSFRS-R rating scores for ALS patients.",
#     "Useful for retrieving specific context from the MetaGPT paper.",
#     "Useful for retrieving specific context from the state of the union speech by the president.",
#     "Useful for retrieving specific context from the Federal Tax Return of 2021 detailing things like gross income, taxable income, tax paid and so on",
#     "Useful for retrieving specific context from Financial Assessment detailing how much to spend per month on various things",
#     "Useful for retrieving specific context from my IELTS result I got in 2023 denoting my English speaking skills",
#     "Useful for retrieving specific context from my resume of 2023 specifying what projects I've worked on, where I studied, what my qualifications are, etc",
#     "Useful for retrieving specific context from my resume of 2024 specifying what projects I've worked on, where I studied, what my qualifications are, etc",
#     "Useful for retrieving specific context from some pointers I've gathered regarding LLMs",
#     "Useful for retrieving specific context from a project I did where I had to do multi-class classification via transfer learning for classifying dog breeds from images",
#     "Useful for retrieving specific context from my project proposal for 'Ivy' master's project with Professor Ashok Goel where we want to build an interactive tutor for incorporating adaptive feedback",
#     "Useful for retrieving specific context from my reflection report at the end of Spring semester in 2024 for Project 'Ivy' - my master's project",
#     "Useful for retrieving specific context from my log of medical tests and conditions over the years",
#     "Useful for retrieving specific context from Pranjali's log of medical tests and conditions over the years",
#     "Useful for retrieving specific context from my bloodwork lab results from 2023",
#     "Useful for retrieving specific context from Pranjali's bloodwork lab results from 2023",
#     "Useful for retrieving specific context from all our trips that Pranjali and myself have taken over the years including trip plans and how much it cost on those trips",
# ]

# vector_indices = []
# for file in input_files:
#     filename = os.path.basename(file).split('.')[0]
#     print (f"Retrieving vector_index for {filename} from storage")
#     storage_context = StorageContext.from_defaults(persist_dir=f"file_embeddings/openAI/{filename}")
#     vector_index = load_index_from_storage(storage_context=storage_context)
#     vector_indices.append(vector_index)
    
# query_engine_tools = []
# for i in range(len(input_files)):
#     query_engine_tools.append(QueryEngineTool.from_defaults(
#         query_engine=vector_indices[i].as_query_engine(),
#         description=file_summaries[i],
#     ))

# query_engine = RouterQueryEngine(
#     selector=LLMSingleSelector.from_defaults(),
#     query_engine_tools=query_engine_tools,
#     verbose=True
# )


@app.route("/jarvis", methods = ['POST'])
def hello_world1():
    data = request.get_json()
    return data['query']
    response = query_engine.query(query)
    return str(response)
