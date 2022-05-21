import socket
from PIL import Image
import sys


HOST = "flood.schenklflut.de"
PORT = 1234
offsetx = 1820
offsety = 0


def main():

    imagename = str(sys.argv[1]) # Adjust this to the name of the iamge

    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Bind the socket to the port
    server_address = (HOST, PORT)
    sock.connect(server_address)
    print("Connected")

    sock.send(b"PX 100 100\n")
    datastream = sock.recv(1024)
    print(datastream.decode())

    im = Image.open(imagename)  # Can be many different formats.
    pix = im.load()
    x, y = im.size #Split the shit into x,y values
    #Parse image into more convenient data type

    pixelarray = [""]

    count = 0

    for i in range(x):
        for j in range(y):

            r, g, b, t = pix[i, j]
            if t != 0:
                count += 1
                pixelarray.append("PX " + str(i+offsetx) + " " + str(j+offsety) + " " + '{:02x}{:02x}{:02x}'.format(r, g, b) + "\n")
                #print(pixelarray[1])

    #Do the actual dump to the server


    while True:

        for i in range(count):

            sock.send(pixelarray[i].encode())
            print(pixelarray[i])


    sock.close()

main()