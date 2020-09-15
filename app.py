from json import dumps
import os

from flask import Flask, render_template, request
from flask_socketio import SocketIO, disconnect
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or '3asFq0MNjA1gkaS2a'
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(os.getcwd(), 'app.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

sio = SocketIO(app, async_mode = 'eventlet')
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class BoardModel(db.Model):
	id = db.Column(db.String(128), primary_key=True)
	body = db.Column(db.Text)

	def __repr__(self):
		return f'Board{self.id} Items: {self.body}'

@app.route('/')
def index():
	return render_template('index.html')

@sio.on('sort', namespace = '/sio')
def sort_text(text):
	words = sorted(list(set(text.split())), key=str.lower)
	sio.emit('new', dumps(words), namespace='/sio')

boards = []

@sio.on('board', namespace='/sio')
def add_word(command):
	print('command', command)
	board = BoardModel.query.filter_by(id = request.sid).first()
	if not board:
		board = BoardModel(id = request.sid, body = '')
	if command == 'LIST':
		print(board.body)
		sio.emit('boards', board.body, namespace='/sio')
	elif command == '':
		db.session.delete(board)
		db.session.commit()
		disconnect(request.sid, '/sio')
	else:
		if board.body == '':
			board.body = command
		else:
			board.body += ',' + command
		db.session.add(board)
		sio.emit('add', command, namespace='/sio')
		db.session.commit()


if __name__ == '__main__':
	sio.run(app, debug=True)