import os
import re
import base64
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


INSTRUCTION = """
You are a intelligent document extraction agent.

You will get an input image from the user, and you have to respond in a structured JSON.
I am attaching the schema for different types of input Images.

Perform OCR on the input image, follow the schema STRICTLY, and respond in JSON format.

IMPORTANT FINAL STEP (MANDATORY):
YOU MUST return the final JSON as the FINAL RESPONSE.

FINAL OUTPUT RULES:
- Return ONLY the JSON object
- No explanations
- No markdown
- No comments
- No extra text
- If a value is missing, return null

RESPONSE EXAMPLE:
Assistant: "Here is the complete response for Image132.png
```json
{
  "invoice": {
    "invoice_number": "89969473",
    "date_of_issue": "10/29/2016",
    "seller": {
      "name": "Johnson-Martin",
      "address": "3836 Moore Ports, North Michael, MO 01844",
      "tax_id": "972-82-0713",
      "iban": "GB71GBDG68039919194335"
    },
    "client": {
      "name": "Deleon, Davila and Allen",
      "address": "355 King Lake Suite 071, South Haleyshire, KY 55765",
      "tax_id": "944-77-3882"
    },
    "items": [
      {
        "no": 1,
        "description": "Wild West Wine",
        "qty": 2.00,
        "unit_of_measure": "each",
        "net_price": 27.00,
        "net_worth": 54.00,
        "vat_percentage": 10,
        "gross_worth": 59.40
      },
      {
        "no": 2,
        "description": "Press Wine 15L Fruit Cider Apple Crusher Juice Grape Stainless Maker Grapes New",
        "qty": 2.00,
        "unit_of_measure": "each",
        "net_price": 279.00,
        "net_worth": 558.00,
        "vat_percentage": 10,
        "gross_worth": 613.80
      }
    ],
    "summary": {
      "vat_percentage": 10,
      "net_worth": 725.37,
      "vat": 72.54,
      "gross_worth": 797.91
    }
  }
}
```
"""


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

    # print(chat_completion.choices[0].message.content)

    return get_json_from_response(chat_completion.choices[0].message.content)


image_path = r"C:\Users\mm0954\Documents\maventic_ai_101\OCR\images\invoice_1.jpg"

with open("output.json", "w") as json_file:
    json_file.write(extract_data_from_image(image_path))

# with open("output.json", "w") as json_file:
#     json_file.write("""{"hello": "world!"}""")

# print(extract_data_from_image(image_path))
