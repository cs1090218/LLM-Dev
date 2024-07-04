# LLM Applications

### RAG
- Retrieval Augmented Generation based Personal Assisstant
- Main code at multi_doc_rag_with_llamaindex.ipynb
    - Reads my files from my Google Drive using google drive api
    - Allows running with gpt-turbo-3.5 using OpenAI api or llama3:instruct (ollama) locally
    - Creates vector embeddings for them and persists in file_embeddings folder to reuse for future use
    - Creates query engine tools for each of the docs using the embeddings and file summaries
    - Uses thes objects to create a router query engine that can route the query to one or more of these query engines

### llm-prompting-with-llama-api
- Samples on how to prompt Llama models using either TogetherAI or the local llama (via ollama)
- A few sample usages of prompting like summarizing, inferring, chatting, etc.

### llm-prompting-with-openai-api
- This uses local llama only (via ollama)
- Some examples of using prompts to accomplish tasks like summarizing, expanding, transforming, etc.

Best to use llm-prompting-with-llama-api for all tasks esp when trying to incorporate it in places. Only use of llm-prompting-with-openai-api is for some sample usages of prompting best practices.
