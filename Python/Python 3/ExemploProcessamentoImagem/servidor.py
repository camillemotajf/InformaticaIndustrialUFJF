import socket
import cv2
import os
import numpy as np

class Servidor():

    def __init__(self, host, port) -> None:
        self._host = host
        self._port = port
        self.__tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Protocolo de comunição entre o servidor

    def start(self): # metodo para inicializar o servidor para uma possível comunicação
        endpoint = (self._host, self._port)
        try:
            self.__tcp.bind(endpoint)
            self.__tcp.listen(1)
            print("Servidor inciado em ", self._host, "na porta: ", self._port)
            while True:
                con, client = self.__tcp.accept()
                self._service(con, client)
        except Exception as e:
            print("Erro ao inicializar o servidor", e.args)

    def _service(self, con, client):
        print("Atendendo ao Cliente: ", client)
        while True:
            try:
                caminho = con.recv(4096) # recebe o caminho da imagem a ser processada em bytes
                caminho = str(caminho.decode('utf-8'))
                img = cv2.imread(caminho)


                # # codificação para bytes
                # _, img_bytes = cv2.imencode('.jpg', img) 
                # img_bytes = bytes(img_bytes)
                # tamanho_da_imagem_codificado = len(img_bytes).to_bytes(4, 'big')

                #  # decodificação
                # tam = int.from_bytes(tamanho_da_imagem_codificado, 'big')
                # img = cv2.imdecode(np.frombuffer(img_bytes, np.uint8), cv2.IMREAD_COLOR)

                # processamento
                xml_classificador = os.path.join(os.path.relpath(
                    cv2.__file__).replace('__init__.py', ''), 'data\haarcascade_frontalface_default.xml')
                face_cascade = cv2.CascadeClassifier(
                    xml_classificador)
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                faces = face_cascade.detectMultiScale(gray, 1.3, 5)

                # Desenha retângulos nas áreas onde as faces foram detectadas
                for (x, y, w, h) in faces:
                    cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)

                # codificando a imagem processada para bytes
                _, img_bytes_p = cv2.imencode('.png', img) 
                img_bytes_p = bytes(img)
                tamanho_da_imagem_codificado_p = len(img).to_bytes(4, 'big')

                # envio a imagem processada em bytes para o cliente
                tupla = (img_bytes_p, tamanho_da_imagem_codificado_p)
                con.send(tupla)
                print(client, "-> requisição atendida")

            except OSError as e:
                print("Erro na conexão ", client, ": ", e.args)
            except Exception as e:
                print("Erro nos dados recebidos pelo cliente ",
                      client, ": ", e.args)
                con.send(bytes("Erro", 'utf-8'))
                return   