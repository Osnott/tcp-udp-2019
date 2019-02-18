import udp_client as client
import client_gui as gui
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

asdadgfasdgjha