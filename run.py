import socket
from cyclofit import create_app

app = create_app()

if __name__ == '__main__':

    hostname = socket.gethostname()
    print(' * Running on :', hostname)
    ip_address = socket.gethostbyname(hostname)

    app.run(debug=True, host=ip_address)