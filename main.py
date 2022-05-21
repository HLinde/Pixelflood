import socket
from PIL import Image


def main():

    imagename = "r37sjR-ohjo.jpg"

    HOST = "flood.schenklflut.de"
    PORT = 1234

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
    size = im.size
    print(size) #Absolutey not necessary only here for fucking testing shit
    x, y = im.size #Split the shit into x,y values
    print(x)
    print(y)
    #print(pix[500, 500])

    for x in range(x):
        for y in range(y):

            print(pix[x, y])
            r, g, b = pix[x, y]
            #print("PX " + str(x) + " " + str(y)+ " " + str(format(r, 'x')) + str(format(g, 'x')) + str(format(b, 'x')))
            shittosend = "PX " + str(x) + " " + str(y) + " " + str(format(r, 'x')) + str(format(g, 'x')) + str(format(b, 'x'))
            sock.send(shittosend.encode())


    sock.close()

main()