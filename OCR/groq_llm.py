import os
import re
import base64
from groq import Groq
from dotenv import load_dotenv
from instruction import INSTRUCTION

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')


def get_json_from_response(content):
    match = re.search(r"```[^\n]*\n([\s\S]*?)\n```", content)
    if match:
        return match.group(1)

    return content


def extract_data_from_image(abs_image_path: str) -> str:
    base64_image = encode_image(abs_image_path)

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": [
                    {"type": "text", "text": INSTRUCTION}
                ],
            },
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Apply extraction on this image"},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}",
                        },
                    },
                ],
            }
        ],
        model="meta-llama/llama-4-scout-17b-16e-instruct",
    )

    return get_json_from_response(chat_completion.choices[0].message.content)


if __name__ == "__main__":
    image_path = r"C:\Users\mm0954\Documents\maventic_ai_101\OCR\images\invoice_1.jpg"

    res = extract_data_from_image(image_path)

    print(res)

    with open("output.json", "w") as json_file:
        json_file.write(res)
