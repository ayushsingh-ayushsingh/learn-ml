import numpy as np
import dspy
from mem import MemoryType

embed = dspy.Embedder(model="ollama/nomic-embed-text-v2-moe:latest")


def generate_embeddings(strings: list[MemoryType]):
    embeddings = embed(strings)
    print(f"Embeddings: {np.array(embeddings).shape}")
    return embeddings


if __name__ == "__main__":
    embeddings = generate_embeddings(
        ["Ayush Singh", "Ayush Singh likes Samosa"])
    print(embeddings)
