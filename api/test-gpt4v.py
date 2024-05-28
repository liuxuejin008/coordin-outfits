import base64
import requests

# OpenAI API Key
api_key = "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"

# Function to encode the image
def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')

# Path to your image
image_path = "./123456.jpg"

# Getting the base64 string
base64_image = encode_image(image_path)
print(len(base64_image))
headers = {
  "Content-Type": "application/json",
  "Authorization": f"Bearer {api_key}"
}

payload = {
  "model": "openai/gpt-4o",
  "messages": [
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": "描述图片的内容"
        },
        {
          "type": "image_url",
          "image_url": {
            "url": f"data:image/jpeg;base64,{base64_image}"
          }
        }
      ]
    }
  ],
  "max_tokens": 300
}
response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=payload)
json_data = response.json()
content = json_data['choices'][0]['message']['content']
print(content)