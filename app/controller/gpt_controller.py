from flask import Blueprint, request, jsonify, Response, make_response, abort
from flask_jwt_extended import jwt_required,get_jwt_identity
from interceptor.sse_client import SSEClient
from service.apple_uniqe_user_service import verify_jwt_token
import requests
import openai
import os
import random

gpt_controller = Blueprint('gpt', __name__)

openai.api_base = "https://ack.fairywoobang.com/v1"

@gpt_controller.route('/completions', methods=['POST'])
@jwt_required()
def openaiCompletions():

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

def prepare_chat_properties(data):
    # channelSubject = data.get("channelSubject")
    temperature = data.get("temperature")
    topProbabilityMass = data.get("topProbabilityMass")
    
    # if channelSubject: 
    #     print(channelSubject) 
    # else:
    #     channelSubject = ""
    if temperature:
        print(temperature) 
    else:
        temperature = 1
    if topProbabilityMass:
        print(topProbabilityMass)
    else:
        topProbabilityMass = 1

    return {
        # "channelSubject": channelSubject,
        "temperature":temperature,
        "topProbabilityMass":topProbabilityMass
    }

@gpt_controller.route('/proxy/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def proxy(path):
    # url = request.url.replace(request.host_url, 'https://api.openai.com/')
    url = request.url.replace(request.host_url, 'https://ack.fairywoobang.com/')
    stream = None
    try:
        stream = request.get_json().get('stream', None)
    except:
        pass

    if "/proxy" in url:
        url = url.replace('/proxy', '')
    
    resp = requests.request(
        method=request.method,
        url=url,
        stream=stream,
        headers={key: value for (key, value)
                 in request.headers if key != 'Host'},
        data=request.get_data(),
        allow_redirects=False)
    if not stream:
        excluded_headers = ['content-encoding',
                            'content-length', 'transfer-encoding', 'connection']
        headers = [(name, value) for (name, value) in resp.raw.headers.items(
        ) if name.lower() not in excluded_headers]
        response = make_response((resp.content, resp.status_code, headers))
        return response

    def stream_generate():
        client = SSEClient(resp)
        for event in client.events():
            yield ('data: ' + event.data + '\n\n')
    return Response(stream_generate(), mimetype='text/event-stream')


@gpt_controller.route('/v1/chat/completions', methods=['POST'])
@jwt_required()
def chat_stream():
    current_user = get_jwt_identity()
    auth_header = request.headers.get("Authorization")
    jwt_token = auth_header.split(" ")[1]  # Assuming JWT is in the format "Bearer <JWT>"
    result = verify_jwt_token(unique_user_id=current_user, jwt = jwt_token)
    if result == False:
        abort(401)

    data = request.get_json()
    messages = data.get("messages")
    if messages:
        print(messages)
    else:
        return jsonify({"success":-1, "message":"message is empty"})
    
    properties = prepare_chat_properties(data)

    openai.api_key = randomOpenAIApiKey()
    # print(temperature)
    # print(topProbabilityMass)
    
    # message = response.choices[0].text.strip()
    def stream():
        completion = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=messages,
                stream=True, 
                max_tokens=1024,
                n=1,
                stop=None,
                temperature=properties.get("temperature"),
                top_p=properties.get("topProbabilityMass"),
            )
        for line in completion:
            # print(line)
            yield 'data: %s\n\n' % line
            # chunk = line['choices'][0].get('delta', {}).get('content', '')
            # if chunk:
            #     print(chunk)
            #     yield 'data: %s\n\n' % chunk
    return Response(stream(), mimetype='text/event-stream')
    # def stream_generate():
    #     completion = openai.ChatCompletion.create(
    #             model="gpt-3.5-turbo",
    #             messages=messages,
    #             stream=True, 
    #             max_tokens=1024,
    #             n=1,
    #             stop=None,
    #             temperature=properties.get("temperature"),
    #             top_p=properties.get("topProbabilityMass"),
    #         )
    #     client = SSEClient(completion)
    #     for event in client.events():
    #         yield ('data: ' + event.data + '\n\n')
    # return Response(stream_generate(), mimetype='text/event-stream')


@gpt_controller.route('/chat', methods=['POST'])
@jwt_required()
def chat():
    data = request.get_json()
    messages = data.get("messages")
    if messages:
        print(messages)
    else:
        return jsonify({"success":-1, "message":"message is empty"})
    properties = prepare_chat_properties(data)

    openai.api_key = randomOpenAIApiKey()
    # print(temperature)
    # print(topProbabilityMass)
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=properties.get("temperature"),
        top_p=properties.get("topProbabilityMass")
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
