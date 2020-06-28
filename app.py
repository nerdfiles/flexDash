#!/usr/bin/env python3
from threading import Lock
from flask import Flask, render_template, url_for, session, request, copy_current_request_context
from flask_socketio import SocketIO, emit

async_mode = None

app = Flask(__name__, template_folder="templates")
app.config['SECRET_KEY'] = 'secret!'

socketio = SocketIO(app, async_mode=async_mode)

thread = None
thread_lock = Lock()

def background_thread():
    """Example of sending server generated events to clients using timed counter"""
    count = 0
    while True:
        socketio.sleep(1)
        count += 1
        socketio.emit('server_message', {'data': 'Server generated event', 'count': count})

@app.route('/')
def index():
    return render_template('index.html', title='Flasky Dash!', async_mode=socketio.async_mode)

@app.route('/grid')
def grid():
    return render_template('grid.html', title="Griddy Dash!", next_dash="test-dash-panel.html", async_mode=socketio.async_mode)

@app.route('/block')
def test_block():
    return render_template("dash/block-dash-panel.html")

@app.route('/Water')
def water():
    return render_template("dash/water.html")

@app.route('/Climate')
def climate():
    return render_template("dash/climate.html")

@app.route('/Network')
def network():
    return render_template("dash/network.html")

@app.route('/Media')
def media():
    return render_template("dash/media.html")

@socketio.on('connect')
def connect():
    global thread
    with thread_lock:
        if thread is None:
            thread = socketio.start_background_task(background_thread)
    emit('server_message', {'data' : 'Connected', 'count' : 0})
