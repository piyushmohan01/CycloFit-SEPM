import socket
from cyclofit import create_app

app = create_app()

if __name__ == '__main__':

    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)

    app.run(debug=True)
    
    # , host='http://192.168.1.103:5000/') - EXT
    # , host='http://192.168.1.3:5000/') - MAIN