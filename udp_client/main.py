import udp_client
import client_gui
import client_handler
import sys

print("Ver: 1.5a")
udp_client.start()

while True:
    if client_handler.failedInit:
        udp_client.close()
        client_gui.reopen()
        udp_client.start()
    elif udp_client.exited:
        udp_client.close()
        sys.exit(0)
