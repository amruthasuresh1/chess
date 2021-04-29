#Server.py
from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO
app = Flask(__name__)
# app.config['SECRET_KEY'] = "Social Distance Secret"
socket_app = SocketIO(app)


@socket_app.on('connected')
def handle_id(data):
    print("Client connected")
    print(data)
    print("sid",request.sid)

if __name__ == '__main__':
    socket_app.run(app, debug=True, host='127.0.0.1', port=3000)
