"""module to interact with expressvpn"""
import subprocess
import Parser
from Server import Server

class Preferences:
    auto_connect = False
    prefered_protocol = ""
    send_diagnostics = True

    def __init__(self, auto_connect, prefered_protocol, send_diagnostics):
        self.auto_connect = auto_connect
        self.prefered_protocol = prefered_protocol
        self.send_diagnostics = send_diagnostics


class Expressvpn:
    connection_status = False
    current_server = None
    servers = {}
    protocols = ["udp", "auto", "tcp"]
    last_server = None

    def __init__(self):
        self.status()
        self.ls()
        self.last_server = self.ls_recent()[0]
        self.preferences()

    def preferences(self):
        output = subprocess.check_output(
            ["expressvpn", "preferences"]).decode("utf-8")
        autoconnect, prefered_protocol, send_diagnostics = Parser.parse_preferences(output)
        self.preferences = Preferences(autoconnect, prefered_protocol, send_diagnostics)

    def autoconnect(self):
        subprocess.call(["expressvpn", "autoconnect"])

    def protocol(self, protocol="auto"):
        subprocess.call(["expressvpn", "protocol", protocol])

    def status(self):
        stream = subprocess.check_output(
            ["expressvpn", "status"]).decode('utf-8')
        if "Not connected" in stream:
            self.connection_status = False
        else:
            self.current_server = Parser.parse_status(stream)

            self.connection_status = True

    def connect(self, server=None):
        print("Attempting to Connect")

        if server is not None:
            stream = subprocess.call(["expressvpn", "connect", server.alias])
            self.current_server = server
        else:
            stream = subprocess.call(["expressvpn", "connect"])
        if stream == 0 or 1:
            self.connection_status = True
            print("Connection Success")

    def disconnect(self):
        stream = subprocess.call(["expressvpn", "disconnect"])
        if stream == 0 or 1:
            print("Disconnect Success")
            self.connection_status = False

    def ls(self):
        output = subprocess.check_output(["expressvpn", "ls"]).decode('utf-8')
        self.servers = Parser.parse_ls(output)

    def ls_recent(self):
        output = subprocess.check_output(
            ["expressvpn", "ls", "recent"]).decode('utf-8')
        recent_servers = Parser.parse_ls_recent(output)
        return recent_servers

    def refresh(self):
        output = subprocess.call(["expressvpn", "refresh"])
        if output == 0:
            return True


if __name__ == "__main__":
    # Example of usage
    express = Expressvpn()
    express.preferences()
