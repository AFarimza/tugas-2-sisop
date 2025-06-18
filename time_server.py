import socket
import threading
import logging
from datetime import datetime

class ProcessTheClient(threading.Thread):
    def __init__(self, connection, address):
        self.connection = connection
        self.address = address
        threading.Thread.__init__(self)

    def run(self):
        logging.warning(f"[CONNECTED] Client dari {self.address}")
        try:
            while True:
                data = self.connection.recv(1024)
                if not data:
                    break
                message = data.decode('utf-8').strip()
                logging.warning(f"[RECEIVED] {message} dari {self.address}")

                if message == "TIME":
                    now = datetime.now()
                    jam = now.strftime("%H:%M:%S")
                    response = f"JAM {jam}\r\n"
                    self.connection.sendall(response.encode('utf-8'))
                elif message == "QUIT":
                    break
                else:
                    self.connection.sendall("Perintah tidak dikenali\r\n".encode('utf-8'))
        except Exception as e:
            logging.error(f"[ERROR] {e}")
        finally:
            self.connection.close()
            logging.warning(f"[DISCONNECTED] {self.address}")

class Server(threading.Thread):
    def __init__(self):
        self.the_clients = []
        self.my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        threading.Thread.__init__(self)

    def run(self):
        self.my_socket.bind(('0.0.0.0', 45000))
        self.my_socket.listen(5)
        logging.warning("[STARTED] Server listening di port 45000...")
        while True:
            self.connection, self.client_address = self.my_socket.accept()
            clt = ProcessTheClient(self.connection, self.client_address)
            clt.start()
            self.the_clients.append(clt)

def main():
    svr = Server()
    svr.start()

if __name__ == "__main__":
    logging.basicConfig(level=logging.WARNING, format='%(asctime)s - %(message)s')
    main()
