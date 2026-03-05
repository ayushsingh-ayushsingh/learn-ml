import os
from dotenv import load_dotenv
from mem0 import Memory

load_dotenv()

config = {
    "llm": {
        "provider": "litellm",
        "config": {
            "model": "groq/openai/gpt-oss-20b",
            "temperature": 0.2,
            "max_tokens": 2000,
        }
    },
    "embedder": {
        "provider": "ollama",
        "config": {
            "model": "embeddinggemma:latest"
        }
    },
    "vector_store": {
        "provider": "qdrant",
        "config": {
            "collection_name": "test",
            "host": "localhost",
            "port": 6333,
            "embedding_model_dims": 768
        }
    }
}

m = Memory.from_config(config)
messages = [
    {"role": "user", "content": "I'm planning to watch a movie tonight. Any recommendations?"},
    {"role": "assistant", "content": "How about thriller movies? They can be quite engaging."},
    {"role": "user", "content": "I’m not a big fan of thriller movies but I love sci-fi movies."},
    {"role": "assistant", "content": "Got it! I'll avoid thriller recommendations and suggest sci-fi movies in the future."}
]
m.add(messages, user_id="john")

res = m.search(query="what would you like to have", user_id="john", limit=3)

print(res)
