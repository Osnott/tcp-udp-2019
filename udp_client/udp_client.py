import cv2
import sys
from client_handler import openServer, recvData, decodeData, initRecvData, FrameQueue
import client_gui
import threading
import time

exited = False


def run(sock, buffer, queue):
    while True:
        queue.put(recvData(sock, buffer))


def start():
    global exited
    while not client_gui.ready:
        if client_gui.exited:
            sys.exit(0)
    UDP_IP = str(client_gui.serverData["ip"])
    UDP_PORT = int(client_gui.serverData["port"])
    DEBUG = client_gui.serverData["debug"]
    print("CONNECTING TO " + UDP_IP + " ON PORT " + str(UDP_PORT))
    client = openServer(UDP_IP, UDP_PORT)
    font = cv2.FONT_HERSHEY_SIMPLEX
    queue = FrameQueue(2)
    threadedFrames = threading.Thread(target=run, args=(client["sock"], 65536, queue))
    if initRecvData(client["sock"], 65536) != b"":
        threadedFrames.daemon = True
        threadedFrames.start()
        time.sleep(0.5)
        while True:
            try:
                client["recv_packet"], decimg = decodeData(queue._get())
            except EOFError:
                print("ERROR! CONNECTION LOST OR SERVER NOT OPEN!\n")
                print("EXITING")
                sys.exit(0)
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
            cv2.imshow("Jetson Camera", decimg)
            height, width, channels = decimg.shape
            cv2.resizeWindow("Jetson Camera", width, height)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                print("\n--------------EXITING--------------\n")
                exited = True
                break


def close():
    cv2.destroyAllWindows()
