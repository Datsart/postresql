from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import requests
from healthcheck import HealthCheck

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://artemdatsenko:19980723@localhost:5432/log_info'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

health = HealthCheck()


class LogInfo(db.Model):
    __tablename__ = 'api_data'

    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    value = db.Column(db.Float, nullable=False)


@app.route('/sendmsg', methods=['POST'])
def send_message():
    # score = request.form.get('score')
    data = request.get_json()
    score = float(data['score'])
    log_info = LogInfo(value=score)
    db.session.add(log_info)
    db.session.commit()

    return jsonify({"score": score})


@app.route('/healthcheck', methods=['GET'])
def healthcheck():
    health_status = health.run()
    return jsonify({"healthcheck": health_status})


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5050, debug=True)
