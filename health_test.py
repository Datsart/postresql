
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
    return 'OK'


def run_flask():
    app.run(host='127.0.0.1', port=int(os.environ.get('PORT', 8000)))


if __name__ == '__main__':
    flask_thread = Thread(target=run_flask)
    flask_thread.start()
