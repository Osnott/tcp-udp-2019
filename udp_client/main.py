import udp_client
import client_gui
import client_handler
import sys

print("Ver: 1.5a")
udp_client.start()

while True:  # runs until exited
    if client_handler.failedInit:  # checks if the client did not connect properly
        udp_client.close()
        client_gui.reopen()
        udp_client.start()
    elif udp_client.exited:  # checks if client was exited by user
        udp_client.close()
        sys.exit(0)
