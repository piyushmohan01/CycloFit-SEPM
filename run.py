import socket
from cyclofit import create_app

app = create_app()

def get_ip():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        sock.connect(('10.255.255.255', 1))
        IP = sock.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        sock.close()
    return IP

if __name__ == '__main__':

    hostname = socket.gethostname()
    print(' * Running on :', hostname)
    ip_address = get_ip()
    print(' * Local IPv4 Addreess :', ip_address)
    app.run(debug=False, host=ip_address)
