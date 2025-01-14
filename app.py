import json
import logging

from flask import Flask, request, render_template

from app_util import chat

logger = logging.getLogger(__file__)

app = Flask(__name__)


@app.route('/')
def hello_world():  # put application's code here
    return render_template('chat.html')


userinfo_data = {}


def get_userinfo(username):
    userinfo = userinfo_data.get(username)
    if not userinfo:
        userinfo = {'username': username, 'history': []}
        userinfo_data[username] = userinfo
    return userinfo


@app.route('/chat', methods=['POST', "GET"])
def robot_chat():
    if request.get_json():
        msg = request.get_json().get('msg')
        username = request.get_json().get('username')
        if username:
            userinfo = get_userinfo(username)
            try:
                text, userinfo['history'] = chat.chat(userinfo, msg)
                print(f"{username}:{msg}   robot:{text}")
            except Exception as e:
                userinfo['history'] = []
                text = ''
                print(f"error {username}:{msg}   robot:{text} {e}")
            return json.dumps({'username': username, 'replay': text})


def chat_test():
    while True:
        userinfo = {'username': 'test', 'history': []}
        try:

            text, userinfo['history'] = chat.chat(userinfo, input('<<'))
            print(f">>robot:{text}")
        except Exception as e:
            userinfo['history'] = []
            text = ''
            print(f"robot:{text} {e}")


if __name__ == '__main__':
    # chat_test()
    app.run(host='0.0.0.0', port=23688, debug=False)
