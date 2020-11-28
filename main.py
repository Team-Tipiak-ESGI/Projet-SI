import json
from bottle import route, run, static_file, get
from bottle_websocket import GeventWebSocketServer
from bottle_websocket import websocket
import subprocess


@get('/websocket', apply=[websocket])
def echo(ws):
    while True:
        msg = ws.receive()

        if msg is not None:
            instructions = json.loads(msg)

            # Write hash to file
            f = open("john/passwd", "w")
            f.write(instructions['chaine'])
            f.close()

            # Run command
            command = 'cd john && john --format={} passwd'.format(instructions['method'])
            print(command)
            p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)

            # Send command output to client via WebSocket
            while True:
                line = p.stdout.readline()
                ws.send(line)
                if not line:
                    break
        else:
            break


@route('/')
def index():
    return static_file('index.html', root='./static', mimetype='text/html')


run(host='localhost', port=8080, server=GeventWebSocketServer)
