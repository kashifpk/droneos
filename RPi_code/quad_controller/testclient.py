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

    sock.sendall("75 0 0\n\n")
    time.sleep(3)
    sock.sendall("65 0 0\n\n")
    time.sleep(1)
    sock.sendall("50 0 0\n\n")
    time.sleep(1)
    sock.sendall("40 0 0\n\n")
    time.sleep(1)
    sock.sendall("30 0 0\n\n")
    time.sleep(1)
    sock.sendall("20 0 0\n\n")
    time.sleep(1)
    sock.sendall("10 0 0\n\n")
    time.sleep(1)
    sock.sendall("0 0 0\n\n")
