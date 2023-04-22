import paramiko
from scp import SCPClient

def createSSHClient(server, port, user, password):
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(server, port, user, password)
    return client
server = "192.168.143.239"
port = 22
user = "pi"
password = "tausat1234"
filename = r"C:\Users\ACER\Desktop\QR.png"
ssh = createSSHClient(server, port, user, password)
scp = SCPClient(ssh.get_transport())
scp.put(filename.encode('unicode_escape'), "/home/pi/Video")
