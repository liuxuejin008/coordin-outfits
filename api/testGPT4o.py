from openai import OpenAI

# gets API Key from environment variable OPENAI_API_KEY
client = OpenAI(
  base_url="https://openrouter.ai/api/v1",
  api_key="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",
)

import base64

IMAGE_PATH = "./123456.jpg"

# Open the image file and encode it as a base64 string
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

base64_image = encode_image(IMAGE_PATH)

def test():
    response = client.chat.completions.create(
        model="openai/gpt-4o",
        messages=[
            {"role": "system", "content": "You are a helpful outfits assistant"},
            {"role": "user", "content": [
                {"type": "text", "text": "Based on the picture, can you give some fashion advice??"},
                {"type": "image_url", "image_url": {
                    "url": f"data:image/jpg;base64,{base64_image}"}
                 }
            ]}
        ],
        temperature=0.0,
    )
    print(response)
    print(response.choices[0].message.content)


def gpt4vstream():
    res = client.chat.completions.create(
        model="openai/gpt-4o",
        messages=[
            {"role": "system", "content": "You are a helpful outfits assistant"},
            {"role": "user", "content": [
                {"type": "text", "text": "Based on the picture, can you give some fashion advice?"},
                {"type": "image_url", "image_url": {
                    "url": f"data:image/jpg;base64,{base64_image}"}
                 }
            ]}
        ],
        temperature=0.8,
        # max_tokens=1000,
        stream=True
    )

    aaa = ""
    for trunk in res:
        json_data = trunk.to_dict()
        if json_data.get('usage') is not None:
            print(json_data['usage']['total_tokens'])
        if trunk.choices[0].finish_reason is not None:
            print('111111111111111')
            data = '[DONE]'
        else:
            print('22222222222222')
            data = trunk.choices[0].delta.content
            print(data)
        aaa = aaa + data

gpt4vstream()
