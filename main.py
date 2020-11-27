from bottle import route, run, static_file, get
from bottle_websocket import GeventWebSocketServer
from bottle_websocket import websocket
import subprocess


@get('/websocket', apply=[websocket])
def echo(ws):
    while True:
        msg = ws.receive()

        if msg is not None:
            print(msg)
            """if msg == 'dir':
                p = subprocess.Popen('john --format=raw-sha256 qwerty', stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)

                while True:
                    line = p.stdout.readline()
                    ws.send(line)
                    if not line:
                        break"""
        else:
            break


@route('/')
def index():
    return static_file('index.html', root='./static', mimetype='text/html')


run(host='localhost', port=8080, server=GeventWebSocketServer)
