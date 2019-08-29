from flask import Flask
from flask_api import status
import socket
import os
import sys

app = Flask(__name__)

disabled = False

@app.route('/')
def k8s_env():
    my_hostname =        socket.gethostname()
    my_address =         socket.gethostbyname(my_hostname)

    if disabled:
        return 'Service disabled @'+my_hostname+'@'+my_address, status.HTTP_503_SERVICE_UNAVAILABLE

    message = '<h1>Kubernetes Environment Information v1</h1>\n'
    message += '<h2>My hostname is '+my_hostname+'</h2>\n'
    message += '<h2>My IP Address is '+my_address+'</h2>\n'
    message += '<h3>Environment Variables:</h3>'
    message += '<table>\n'
    message += '<tr> <th>Environment Variable</th> <th>Value</th> </tr>\n'
    for variable in os.environ.keys():
        message += '<tr> <td>'+variable+'</td> <td>'+os.environ.get(variable)+'</td> </tr>\n'
    message += '</table>\n'

    return message

@app.route('/disable')
def disable():
    global disabled
    disabled = True
    my_hostname =        socket.gethostname()
    my_address =         socket.gethostbyname(my_hostname)
    return '<h2>Disabling '+my_hostname+'@'+my_address+'</h2>'

@app.route('/healthcheck')
def healtcheck():
    global disabled
    if disabled:
        return 'Service disabled', status.HTTP_503_SERVICE_UNAVAILABLE
    else:
        return 'OK', status.HTTP_200_OK

if __name__ == '__main__':
    app.run(debug=False,host='0.0.0.0')
