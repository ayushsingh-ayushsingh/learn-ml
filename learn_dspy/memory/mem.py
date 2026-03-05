from typing import List
import os
import dspy
from litellm import json
import asyncio
from embed import generate_embeddings
from pydantic import BaseModel, Field

lm = dspy.LM(
    model="groq/openai/gpt-oss-20b",
    api_key=os.environ.get("GROQ_API_KEY"),
)

dspy.configure(lm=lm)


class MemoryType(BaseModel):
    imformation: str = Field(
        description="Be very very concise, 5 to 10 words, 15 AT MAX")
    predicted_category: List[str] = Field(
        description="Each category should be written in minimum number of words possible 1 to 3 words in snakecase, following smallcase - eg. food_preference, family_relation, personal_information, ownership, general_preferences etc.")


class MemoryExtract(dspy.Signature):
    """
    Extract relavant information from the conversation. Create memory entries that you should remember when speaking with the user later. Each memory is a UNIQUE fact.
    You will get a list of categories from the database, if the information does not fit for any of them you can create your own category. Each fact should be complete in on itself:
    Example: "My name is Ayush Singh and I like Doraemon"
    (1) "User's name is Ayush Singh" -> personal_information -> GOOD
    (2) "User like Doraemon cartoon" -> personal_preference -> BAD (Does not specify who)
    The second one should be "Ayush likes Doraemon cartoon" -> personal_preference -> It is GOOD now
    """
    transcript: str = dspy.InputField()
    existing_categories: list[str] = dspy.InputField(
        description="If there is information, check if there is relavant category for that, if not you may create one yourslef.")
    no_info_flag: bool = dspy.OutputField(
        description="Make it true if there is no important information")
    memories: list[MemoryType] = dspy.OutputField()


memory_extractor = dspy.Predict(MemoryExtract)


async def extract_memories_from_messages(messages, categories):
    transcript = json.dumps(messages)
    with dspy.context(lm=lm):
        out = await memory_extractor.acall(transcript=transcript, existing_categories=categories)
    print(out)
    print("\n")
    print(out.memories)
    return out.memories


def extract_and_embed_memories(messages, categories):
    categories = ["preferences", "food_preferences"]
    memories = extract_memories_from_messages(
        messages=messages, categories=categories)

    embeddings = generate_embeddings()


if __name__ == "__main__":
    categories = ["preferences", "food_preferences"]
    messages = [
        {
            "role": "user",
            "content": "My name is Ayush Singh and I like samosas."
        },
        {
            "role": "assistant",
            "content": "Got it!"
        },
        {
            "role": "user",
            "content": "I like kachoris more now, kachoris with tomato chutney is the best."
        }
    ]
    asyncio.run(extract_memories_from_messages(
        messages=messages, categories=categories))
