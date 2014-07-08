"""
Sockets based interface for controlling the Quad Copter - Server Module
"""

import socket

SERVER_ADDRESS = './quad.sock'



if '__main__' == __name__:

    menu = \
    """
    Set Speed and angle:

        speed x_angle y_angle

    to exit type: quit

    """
    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)

    print('connecting to %s' % SERVER_ADDRESS)
    sock.connect(SERVER_ADDRESS)

    line = ''

    while 'quit' != line.lower().strip():
        line = raw_input('Quad Controller Command > ')
        sock.sendall(line + '\n')

    sock.close()
