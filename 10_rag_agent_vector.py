import asyncio
from pathlib import Path
import uuid

import tiktoken
import chromadb
from agents import Agent, Runner, function_tool

from openai_client import init_client

init_client()

script_text = Path("sample_documents/back_to_the_future.txt").read_text(encoding="utf-8")

def simple_chunk(text, max_tokens=200):
    tokenizer = tiktoken.get_encoding("cl100k_base")
    words, chunk, chunks = text.split(), [], []

    for w in words:
        if (len(tokenizer.encode(" ".join(chunk + [w]))) > max_tokens):
            chunks.append(" ".join(chunk))
            chunk = [w]
        else:
            chunk.append(w)

    if chunk:
        chunks.append(" ".join(chunk))

    return chunks

docs = simple_chunk(script_text, max_tokens=200)
client = chromadb.PersistentClient(path="./tmp/chromadb")

collection_name = "bttf_script"

try:
    collection = client.get_collection(collection_name)
except Exception:
    collection = client.create_collection(name=collection_name)

if collection.count() == 0:
    collection.add(ids=[str(uuid.uuid4()) for _ in docs], documents=docs)

@function_tool
def search_script(query: str, top_k: int=3) -> str:
    res = collection.query(query_texts=[query], n_results=top_k)
    if res and "documents" in res and res["documents"] and res["documents"][0]:
        return "\n\n".join(res["documents"][0])
    return "No relevant documents found"

agent=Agent(
    name="Script Agent",
    instructions=(
        "You answer questions about the movie *Back to the Future*.\n"
        "When needed, call the `search_script` tool to fetch passages, "
        "then cite or paraphrase them in your answer.\n"  
        "Make sure your answers are only from the script text.\n" 
    ),
    tools=[search_script]
)

query = "Where does Doc tell Marty to meet him, and at what time?"
result = Runner.run_sync(agent, query)
print("\n--- ANSWER ---\n", result.final_output)

query = "What happens at 1:15AM"    #7
result = Runner.run_sync(agent, query)
print("\n--- ANSWER ---\n", result.final_output)