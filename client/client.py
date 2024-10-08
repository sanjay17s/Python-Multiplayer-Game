import socket
import json
import threading
from protocols import Protocols


class Client:
    def __init__(self,host="127.0.0.1",port=8000):
        self.nickname = None
        self.server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.server.connect((host,port))

        self.close = False
        self.started = False
        self.questions = []
        self.current_question_index = 0
        self.opponent_question_index = 0
        self.opponent_name = None
        self.winner = None

    def receive(self):
        while not close:
            try:
                data = self.server.recv(1024).decode("ascii")
                message = json.loads(data)
                self.handle_response(message)
            except:
                break
        self.close()

    def start(self):
        receive_thread = threading.Thread(target=self.receive)
        receive_thread.start()

    def send(self, request, message):
        data = {"type": request, "data": message}
        self.server.sendall(json.dumps(data).encode("ascii"))

    def close(self):
        self.close = True
        self.server.close()

    def handle_response(self, response):
        r_type = response.get("type")
        data = response.get("data")

        if r_type == Protocols.Response.QUESTIONS:
            self.questions = data
        elif r_type == Protocols.Response.OPPONENT:
            self.opponent_name = data
        elif r_type == Protocols.Response.OPPONENT_ADVANCE:
            self.opponent_question_index += 1
        elif r_type == Protocols.Response.START:
            self.started = True
        elif r_type == Protocols.Response.WINNER:
            self.winner = data
            self.close()
        elif r_type == Protocols.Response.OPPONENT_LEFT:
            self.close()
        
