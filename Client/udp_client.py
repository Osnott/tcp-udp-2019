import cv2
import sys
import time
from client_handler import openServer, recvData, decodeData, checkLostPackets, calculatePings

UDP_IP = str(sys.argv[1])  # "192.168.43.235"
DEBUG = sys.argv[2] == 'True'
UDP_PORT = 9999
print("CONNECTING TO " + UDP_IP + " ON PORT " + str(UDP_PORT))
sock, pings, packets_lost, start, end, expected_packet, recv_packet = openServer(UDP_IP, UDP_PORT)
font = cv2.FONT_HERSHEY_SIMPLEX

while True:
    start = time.time()
    bytes_data = recvData(sock, 65536)
    end = time.time()
    recv_packet, decimg = decodeData(bytes_data)
    ping = ((end-start) * 1000)
    pings.append(ping)
    top_ping, all_pings = calculatePings(pings)
    if DEBUG:
        cv2.putText(decimg, "Ping: " + str(round(ping)) + "ms", (10, 35), font, 0.5, (255, 255, 255), 1, cv2.LINE_AA)
        cv2.putText(decimg, "Packets Lost: " + str(packets_lost) + " packets", (425, 35), font, 0.5, (255, 255, 255), 1, cv2.LINE_AA)
    cv2.putText(decimg, "Packet Loss: " + str(round((packets_lost/(expected_packet + 1)) * 100)) + "%", (450, 460), font, 0.5, (255, 255, 255), 1, cv2.LINE_AA)
    cv2.putText(decimg, "Average Ping: " + str(round(all_pings/len(pings))) + "ms", (10, 460), font, 0.5, (255, 255, 255), 1, cv2.LINE_AA)
    if ping >= 100:
        cv2.putText(decimg, "HIGH PING!", (250, 35), font, 0.5, (0, 0, 255), 1, cv2.LINE_AA)
    cv2.imshow("Jetson Camera", decimg)
    expected_packet, packets_lost = checkLostPackets(expected_packet, recv_packet, packets_lost)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        print("\n--------------EXITING--------------\n")
        print("Total Pings: " + str(len(pings)) + " pings")
        print("Top Ping: " + str(round(top_ping)) + "ms")
        print("Average Ping: " + str(round(all_pings/len(pings))) + "ms")
        print("Packets Lost: " + str(packets_lost) + " packets")
        print("Packet Loss: " + str(round((packets_lost/expected_packet)*100)) + "%")
        break

cv2.destroyAllWindows()
