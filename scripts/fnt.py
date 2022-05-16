import socket
import requests

def fnt_connected():
    try:
        fnt = socket.create_connection(("www.google.com", 80))
        
        if fnt is not None:
            fnt.close()
            
            return True
    except OSError:
        pass

    return False


def fnt_IP(isConnected: bool):
    if isConnected:
        fnt = socket.socket(socket.AF_INET, socket.SOCK_DGRAM).connect(('8.8.8.8', 0))

        return fnt.getsockname()[0]
    else:
        return False


def fnt_response(isConnected: bool):
    if isConnected:
        response = requests.get("https://www.google.com") 
    
        return response.status_code
    else:
        return False


def fnt_ConnectionError(openIP: bool):
    print()
    print("============ Raised ConnectionError ============")
    print("/- Reconnecting trying - flag requests stopped")
    print("/- Connection condition test - fnt activated")

    isConnected = fnt_connected()
    fntIP = fnt_IP(isConnected)
    fntResponse = fnt_response(isConnected)

    print(f"/- Network connected - {isConnected}")

    if isConnected:
        print("/- Socket created(\"www.google.com\")")
        print(f"/- Request status: {fntResponse}")

        if openIP and fntIP:
            print(f"/- LAN IPv4 address: {fntIP}")
        
        print("/- Socket has been closed")
    else:
        print("/- ***** Network does not connected")

