import cv2
import sys
from client_handler import openServer, recvData, decodeData, initRecvData, FrameQueue
import client_gui
import threading
import time

exited = False


def run(sock, buffer, queue):
    """
    Called by thread to constantly get frames and put them in a queue for other code to access
    """
    while True:
        queue.put(recvData(sock, buffer))  # puts the received packet into a queue


def start():
    global exited
    while not client_gui.ready:  # check if user pressed 'connect' button
        if client_gui.exited:  # check if user exited gui
            sys.exit(0)
    UDP_IP = str(client_gui.serverData["ip"])
    UDP_PORT = int(client_gui.serverData["port"])
    DEBUG = client_gui.serverData["debug"]
    print("CONNECTING TO " + UDP_IP + " ON PORT " + str(UDP_PORT))
    client = openServer(UDP_IP, UDP_PORT)
    font = cv2.FONT_HERSHEY_SIMPLEX
    queue = FrameQueue(2)  # start frame queue
    threadedFrames = threading.Thread(target=run, args=(client["sock"], 65536, queue))  # start frame thread
    if initRecvData(client["sock"], 65536) != b"":  # check if initialization of client has not failed
        threadedFrames.daemon = True  # make sure thread closes after program exits
        threadedFrames.start()  # start the thread
        time.sleep(0.5)  # wait for thread to complete
        while True:
            client["recv_packet"], decimg = decodeData(queue._get())  # decode packet in queue
            if DEBUG:
                cv2.putText(
                    decimg,
                    "Packets Lost: " + str(client["packets_lost"]) + " packets",
                    (425, 35),
                    font,
                    0.5,
                    (255, 255, 255),
                    1,
                    cv2.LINE_AA,
                )
                cv2.putText(
                    decimg,
                    "Packet Loss: " + str(
                        round(
                            (client["packets_lost"] / (client["expected_packet"] + 1)) * 100
                        )
                    ) + "%",
                    (450, 460),
                    font,
                    0.5,
                    (255, 255, 255),
                    1,
                    cv2.LINE_AA,
                )
            cv2.namedWindow("Jetson Camera")
            cv2.imshow("Jetson Camera", decimg)  # show the image
            height, width, channels = decimg.shape
            cv2.resizeWindow("Jetson Camera", width, height)  # resize window to image size
            if cv2.waitKey(1) & 0xFF == ord("q"):  # check if 'q' key was pressed on window
                print("\n--------------EXITING--------------\n")
                exited = True
                break


def close():
    cv2.destroyAllWindows()
