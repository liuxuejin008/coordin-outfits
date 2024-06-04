import base64
import json
import os
import traceback
import uuid
from os.path import dirname, abspath, join
from flask import Blueprint, render_template
index_bp = Blueprint('index', __name__)

import openai
from openai import OpenAI
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from starlette.responses import StreamingResponse
from werkzeug.utils import secure_filename


dir = dirname(abspath(__file__))

upload_folder = './images'
import requests
from flask import  jsonify, request, render_template, Response


client = OpenAI(base_url="https://openrouter.ai/api/v1",
                api_key="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")



@index_bp.route('/home')
def home():
    return 'Hello, World!'


@index_bp.route('/about')
def about():
    return 'About'


@index_bp.route('/list', methods=['GET', 'POST'])
def list():
    try:
        word = request.args.get("word")
        if word is None:
            return jsonify({"message": "empty input", "rcode": 1})
        url = "https://api.together.xyz/v1/chat/completions"
        headers = {
            "Authorization": "Bearer 0c26a4544f9d3e83835161e853a79fc5f82c4ccb156a423f339af516ed11fe24",
            "Content-Type": "application/json"
        }
        prompt = f"""
                   假设你是一个emoji专家，我输入文字，你整理概括输出相关的emoji并输出unicode,并至少输出5个相关emoji。
                   给定的文字: ```{word}```
                   """
        data = {
            "model": "teknium/OpenHermes-2p5-Mistral-7B",
            "messages": [
                {"role": "system", "content": "You are an expert emoji guide"},
                {"role": "user", "content": prompt}
            ]
        }
        response_1 = requests.post(url, headers=headers, json=data)
        if response_1.status_code == 200:
            print("Request successful. Response:")
            print(response_1.json())
            message = response_1.json()["choices"][0]["message"]["content"]
        else:
            print(f"Request failed with status code: {response_1.status_code}")
            print(response_1.text)

        return jsonify({'message': message})
    except Exception as e:
        traceback.print_exc()
        # 发生异常时执行回滚操作
        print(f"An error occurred: {e}")
    return jsonify({"message": message, "rcode": 0})


@index_bp.route('/main.html')
def result():
    dict = {'phy': 50, 'che': 60, 'maths': 70}
    return render_template('main.html', result=dict)



@index_bp.route('/price.html')
def result():
    dict = {'phy': 50, 'che': 60, 'maths': 70}
    return render_template('main.html', result=dict)


@index_bp.route('/stream1')
def stream1():
    def event_stream():
        while True:
            yield 'data: %s\n\n' % 'Hello, World!'

    return Response(event_stream(), mimetype="text/event-stream")




@index_bp.route('/sse.html', methods=['GET'])
def sse():
    return render_template('sse.html', result=dict)


def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")



@index_bp.route('/stream', methods=['GET'])
def stream():

    question = request.args.get("question")
    file_name = request.args.get("fileName")
    print(f"question={question}")
    print(f"file_name={file_name}")
    def event_stream():
        file_path = os.path.join(upload_folder, file_name)
        base64_image = encode_image(file_path)
        print(len(base64_image))
        res = client.chat.completions.create(
            model="openai/gpt-4o",
            messages=[
                {"role": "system", "content": "You are a helpful outfits assistant"},
                {"role": "user", "content": [
                    {"type": "text", "text": question},
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
            if trunk.choices[0].finish_reason is not None:
                print('111111111111111')
                data = '[DONE]'
            else:
                print('22222222222222')
                data = trunk.choices[0].delta.content
                print(data)
            aaa = aaa + data
            yield "data: %s\n\n" % data.replace("\n", "<br>")
        print(aaa)
    response1 = Response(event_stream())
    response1.headers['Content-Type'] = 'text/event-stream'
    return response1


def generate_sse():
    data = "Hello, SSE!"
    event = "message"

    yield "data: {}\n".format(data)
    yield "event: {}\n\n".format(event)


@index_bp.route('/sse')
def sse111():
    response = Response(generate_sse())
    response.headers['Content-Type'] = 'text/event-stream'
    return response


def get_file_type(filename):
    """
    根据文件名获取文件类型（通过扩展名）

    :param filename: 文件名，包含扩展名
    :return: 文件类型（基于扩展名），如果未知则返回'unknown'
    """
    # 使用os.path.splitext分离文件名和扩展名
    extension = os.path.splitext(filename)[1]

    # 创建一个简单的映射，根据扩展名映射到文件类型
    file_types = {
        '.jpg': '.jpg',
        '.jpeg': '.jpeg',
        '.png': '.png',
        # 添加更多类型...
    }

    # 检查扩展名是否在字典中，如果在，则返回对应的文件类型，否则返回'unknown'
    return file_types.get(extension.lower(), 'unknown')


@index_bp.route('/upload', methods=['POST'])
def upload():
    if request.method == 'POST':
        f = request.files['file']
        uuid_filename = str(uuid.uuid4())
        uuid_filename_no_dashes = uuid_filename.replace("-", "")
        file_name = uuid_filename_no_dashes+get_file_type(f.filename)
        print(f"file_name={file_name}")
        file_path = os.path.join(upload_folder, file_name)
        print(f"file_path={file_path}")
        f.save(file_path)
        return jsonify({"message": {"file_name":file_name}, "rcode": 0})
    return jsonify({"message": "Get is not allowed", "rcode": 1})

