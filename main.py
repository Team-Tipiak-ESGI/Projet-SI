import json
from bottle import route, run, static_file, get
from bottle_websocket import GeventWebSocketServer
from bottle_websocket import websocket
import subprocess
from threading import Thread


def send_line(stdout, ws):
    # Send command output to client via WebSocket
    while True:
        line = stdout.readline()
        ws.send(line)
        if not line:
            break


def run_command(command, ws):
    print(command)
    p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)

    t = Thread(target=send_line, args=(p.stdout, ws))
    t.daemon = True  # thread dies with the program
    t.start()


@get('/websocket', apply=[websocket])
def echo(ws):
    methods = ["raw-SHA256", "raw-SHA1", "raw-MD5", "bcrypt", "mysql"]

    while True:
        msg = ws.receive()

        if msg is not None:
            instructions = json.loads(msg)

            # Write hash to file
            f = open("john/passwd", "w")
            f.write(instructions['string'])
            f.close()

            # Verify if method is available
            if not instructions['method'].isnumeric():
                break

            method = int(instructions['method'])
            if not 0 <= method <= 4:
                break

            # Crack passwords
            command = 'cd john && john --format={} passwd'.format(methods[method])
            run_command(command, ws)

            # Show passwords
            command = 'cd john && john --format={} --show passwd'.format(methods[method])
            run_command(command, ws)
        else:
            break


@route('/')
def index():
    return static_file('index.html', root='./static', mimetype='text/html')


@route('/<path:path>')
def index(path):
    return static_file(path, root='./static')


if __name__ == '__main__':
    run(host='localhost', port=8080, server=GeventWebSocketServer)
