#!/usr/bin/env python3

from flask import Flask
from threading import Thread
import os

app = Flask(__name__)


@app.route('/health')
def health_check():
    # Add your custom health check logic here
    if all_required_services_are_running():
        return 'OK', 200
    else:
        return 'Service Unavailable', 500


# Example health check logic, replace it with your actual logic
def all_required_services_are_running():
    # Replace this with your logic to check the health of your services
    # For example, check if the required processes are running
    return True


def run_flask():
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5050, debug=True)
