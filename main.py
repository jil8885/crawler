from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/keyboard')
def keyboard():
    json_data = {"type": "buttons", "buttons": ['열번 조회']}
    return jsonify(json_data)


@app.route('/message', methods=['POST'])
def message():
    received_data = request.get_json()
    content = received_data['content']
    string = content
    button_list = ["열번 조회"]
    json_data = {'message': {'text': string}, 'keyboard': {'type': 'buttons', 'buttons': button_list}}
    return jsonify(json_data)


app.run(host='0.0.0.0')