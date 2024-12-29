import socket
import sys
import logging
from PIL import Image
import numpy as np
from scipy.ndimage import rotate
import matplotlib.pyplot as plt

logger = logging.getLogger(__name__)
FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
logging.basicConfig(format=FORMAT, level="INFO")

if no_gamepad := False:
    def get_gamepad():
        return []
else:
    from inputs import get_gamepad


class Figurine():
    def __init__(self, image_path, initial_position=(0, 0, 0), phi_offset=0):
        self.x, self.y, self.phi = initial_position
        self.phi_offset = phi_offset
        self.vx = self.vy = 0
        im_frame = Image.open(image_path)
        self.raw_image = np.array(im_frame)
        self.image = rotate(self.raw_image, np.rad2deg(self.phi + self.phi_offset))

    def update(self):
        for event in self.get_events():
            logger.debug(event.ev_type, event.code, event.state)
            if event.ev_type == "Absolute":
                input_number = (int(event.state) - 128) / 128
                match event.code:
                    case "ABS_X":
                        self.vx = input_number
                    case "ABS_Y":
                        self.vy = - input_number
        self.update_position()
        self.update_rotation()

    def get_events(self, n=1):
        events = sum((get_gamepad() for i in range(n)), start=[])
        print(events)
        return events

    def update_position(self):
        self.x += self.vx
        self.y += self.vy

    def update_rotation(self):
        absolute_velocity = np.sqrt(self.vx**2 + self.vy**2)
        velocity_scale = 1
        print(absolute_velocity)
        dampening = 1 - min(1, absolute_velocity / velocity_scale)
        print(dampening)
        velocity_phi = - np.rad2deg(np.arctan2(self.vx, self.vy))
        print(velocity_phi)
        print(self.phi)
        self.phi = dampening * self.phi + velocity_phi * (1 - dampening)
        print(self.phi)
        self.image = rotate(self.raw_image, self.phi + self.phi_offset)

    def show(self):
        x_shape, y_shape, _ = self.image.shape
        raw_x, raw_y = np.arange(x_shape), np.arange(y_shape)
        x = raw_x + self.x
        y = raw_y + self.y
        return x, y ,self.image


class PixelFlooder():
    def __init__(self, fig: Figurine, host, port):
        self.moving_figure = fig
        self.host = host
        self.port = port
        if self.dry_run:
            self.fig, self.axes = plt.subplots()
            self.axes.set_aspect("equal")
        else:
            # Create a TCP/IP socket
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # Bind the socket to the port
            self.server_address = (HOST, PORT)
            self.sock.connect(self.server_address)
            print("Connected")

            self.sock.send(b"PX 100 100\n")
            datastream = self.sock.recv(1024)
            print(datastream.decode())

    @property
    def dry_run(self):
        return self.host is None
    
    def update(self):
        self.moving_figure.update()
        if self.dry_run:
            X, Y, C = self.moving_figure.show()
            self.axes.pcolormesh(X, Y, np.transpose(C, axes=(1, 0, 2)))
            plt.pause(0.0001)


HOST = None
PORT = 1234
offsetx = 0
offsety = 0

imagename = str(sys.argv[1]) # Adjust this to the name of the iamge
flooder = PixelFlooder(Figurine(imagename), None, 0)

while True:
    flooder.update()
