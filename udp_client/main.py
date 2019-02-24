from udp_client import start, close
from client_gui import reopen
import client_handler as handler
import sys

client.start()

while True:
    if handler.failedInit:
        client.close()
        gui.reopen()
        client.start()
    elif client.exited:
        client.close()
        sys.exit(0)
