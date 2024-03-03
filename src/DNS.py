import socket

def getIpByHostname(hostname):
    try:
        return socket.gethostbyname(hostname + ".cc")
    except:
        return None
    
def getHostnameByIp(ip):
    try:
        return socket.gethostbyaddr(ip)[0][:-20]
    except:
        return None