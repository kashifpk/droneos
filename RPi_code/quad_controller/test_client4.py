"""
Sockets based interface for controlling the Quad Copter - Server Module
"""

import socket
import time

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

    sock.sendall("85 0 0\n\n")
    time.sleep(10)
    for i in range(1, 86):
        sock.sendall("85-i 0 0\n\n")
        time.sleep(1)
    