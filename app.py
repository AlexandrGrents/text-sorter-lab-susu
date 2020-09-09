from json import dumps

from flask import Flask, render_template, request
from flask_socketio import SocketIO, disconnect

app = Flask(__name__)
sio = SocketIO(app, async_mode = 'eventlet')

@app.route('/')
def index():
	return render_template('index.html')

@sio.on('sort', namespace = '/sio')
def sort_text(text):
	words = sorted(list(set(text.split())), key=str.lower)
	sio.emit('new', dumps(words), namespace='/sio')

boards = []

@sio.on('board', namespace='/sio')
def board(command):
	print('command', command)
	global boards
	if command == '':
		disconnect(request.sid, '/sio')
	elif command == 'LIST':
		sio.emit('boards', dumps(boards), namespace='/sio')
	else:
		boards.append(command)
		sio.emit('add', command, namespace='/sio')

if __name__ == '__main__':
	print('run')
	sio.run(app, debug=True)