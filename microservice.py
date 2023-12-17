from flask import Flask, request, jsonify
import random

app = Flask(__name__)


@app.route('/sendmsg', methods=['POST'])
def send_message():
    score = request.form.get('score')

    return jsonify({"score": score})


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5050)
