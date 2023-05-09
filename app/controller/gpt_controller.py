from flask import Blueprint, request, jsonify
# from flask_jwt_extended import create_access_token,jwt_required,get_jwt_identity

import openai
import os
import random

gpt_controller = Blueprint('gpt', __name__)

@gpt_controller.route('/completions', methods=['POST'])
def openaiCompletions():
    
    #TODO 限流

    data = request.get_json()
    input_msg = data["message"]

    openai.api_key = randomOpenAIApiKey()
    response = openai.Completion.create(
        engine="text-davinci-003",
        # engine="gpt-3.5-turbo",
        prompt=input_msg,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=1,
    )
    # print(response)
    #TODO: 增加数据统计
    message = response.choices[0].text.strip()
    return jsonify({"message": message})

@gpt_controller.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    messages = data.get("messages")
    channelSubject = data.get("channelSubject")
    temperature = data.get("temperature")
    topProbabilityMass = data.get("topProbabilityMass")
    if messages:
        print(messages)
    else:
        return jsonify({"success":-1, "message":"message is empty"})
    if channelSubject: 
        print(channelSubject) 
    else:
        channelSubject = ""
    if temperature:
        print(temperature) 
    else:
        temperature = 1
    if topProbabilityMass:
        print(topProbabilityMass)
    else:
        topProbabilityMass = 1

    openai.api_key = randomOpenAIApiKey()
    
    # print(temperature)
    # print(topProbabilityMass)
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=temperature,
        top_p=topProbabilityMass
    )
    
    # message = response.choices[0].text.strip()
    return response


def randomOpenAIApiKey():
    apikeys = os.environ.get("OPENAI_API_KEY")
    if apikeys:
        apiKeyList = apikeys.split(",") 
        if apiKeyList:     
            return random.choice(apiKeyList)

    return ""
