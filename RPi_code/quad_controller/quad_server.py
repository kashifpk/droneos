"""
Sockets based interface for controlling the Quad Copter - Server Module
"""

import time
from quad_controller import QuadCopter
from motor import ServoMotor

import socket
import errno
import sys
import os
from threading import Thread

SERVER_ADDRESS = './quad.sock'

class DroneController(object):
    """
    Class to control a drone
    """

    def __init__(self):

        self.server_sock = None
        self.balancer_thread = None
        self.stop_balancing = False
        self.drone = None
        self.average_speed = 0
        self.angle_x = 0
        self.angle_y = 0


    def setup_drone(self):
        "Setup drone motors, create drone object and make it ready for startup"

        m_FL = ServoMotor(18, "front-left")
        m_FR = ServoMotor(23, "front-right")
        m_RL = ServoMotor(24, "rear-left")
        m_RR = ServoMotor(25, "rear-right")

        self.drone = QuadCopter(m_FL, m_FR, m_RL, m_RR)

        self.drone.start()
        print("Ready for operation!!!")

    def _drone_balancer(self):
        """
        This method keeps balancing the drone accordign to current vector
        """

        print("Drone balancer running!")
        while not self.stop_balancing:
            print("*Drone balancer*")
            self.drone.maintain_vector(self.average_speed,
                                       self.angle_x,
                                       self.angle_y)
            #print(self.drone)
            time.sleep(0.1)

    def _handle_client_connection(self, client_connection):
        "Handle a client connection"

        try:
            print('connected to client')

            self.balancer_thread = Thread(
                target=DroneController._drone_balancer,
                args=(self, ))
            self.balancer_thread.start()

            while True:
                client_connection.setblocking(0)
                sock_file = client_connection.makefile()
                #line = connection.recv(1024)
                try:
                    line = sock_file.readline()
                    line = line.strip()
                    if line:
                        #print(line)
                        # line either contains quit or instructions of the form:
                        # average_speed x_angle y_angle
                        if 'quit' == line.lower():
                            self.stop_balancing = True
                            break

                        parts = line.split(' ')
                        if 3 != len(parts):
                            print("ERROR: Invalid instruction: %s" % line)
                        else:
                            avg_speed, rot_x, rot_y = [int(i) for i in parts]

                            self.average_speed = avg_speed
                            self.angle_x = rot_x
                            self.angle_y = rot_y

                except socket.error, err:
                    if err.args[0] == errno.EWOULDBLOCK:
                        #print('EWOULDBLOCK')
                        time.sleep(0.2)  # short delay, no tight loops
                    else:
                        print(err)
                        break

        finally:
            # Clean up the connection
            if self.balancer_thread:
                self.balancer_thread.join()
                self.balancer_thread = None

            client_connection.close()

    def start_server(self, socket_address):
        """
        Start a listening unix domain socket used for receiving
        drone control instructions
        """
        try:
            os.unlink(socket_address)
        except OSError:
            if os.path.exists(socket_address):
                raise

        self.server_sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)

        print('starting up on %s' % socket_address)
        self.server_sock.bind(socket_address)

        # Listen for incoming connections
        self.server_sock.listen(1)

        while True:
            # Wait for a connection
            print('waiting for a connection')
            connection, client_address = self.server_sock.accept()
            self._handle_client_connection(connection)


if '__main__' == __name__:

    # Make sure the socket does not already exist
    drone_controller = DroneController()
    drone_controller.setup_drone()
    drone_controller.start_server(SERVER_ADDRESS)
