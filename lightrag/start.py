import os
from lightrag import LightRAG, QueryParam
from lightrag.llm import gpt_4o_mini_complete  # Replace with your LLM if needed

WORKING_DIR = "./dickens"

if not os.path.exists(WORKING_DIR):
    os.mkdir(WORKING_DIR)

rag = LightRAG(
    working_dir=WORKING_DIR,
    llm_model_func=gpt_4o_mini_complete  # Default: gpt_4o_mini_complete
)

# Insert data into LightRAG
with open("./book.txt") as f:
    rag.insert(f.read())

# Perform various searches
print(rag.query("What are the top themes in this story?", param=QueryParam(mode="naive")))
print(rag.query("What are the top themes in this story?", param=QueryParam(mode="local")))
print(rag.query("What are the top themes in this story?", param=QueryParam(mode="global")))
print(rag.query("What are the top themes in this story?", param=QueryParam(mode="hybrid")))

