import socket
import cv2
import numpy as np

class Cliente():
    def __init__(self, server_ip, port):
        self.__server_ip = server_ip
        self.__port = port
        self.__tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def start(self, caminho):
        endpoint = (self.__server_ip, self.__port)
        try:
            self.__tcp.connect(endpoint)
            print("Conexão Realizada com Sucesso!")
            self.__method(caminho)
        except:
            print('Servidor não disponível')

    def __method(self, caminho):
        try:

            img = cv2.imread(caminho) # le a imagem do caminho

            if img is None:
                print(f"Error loading image: {caminho}")
            else:
                print("Image loaded successfully")

            # codifica para bytes
            _, img_bytes = cv2.imencode('.jpg', img) 
            img_bytes = bytes(img_bytes)
            tam_bytes= len(img_bytes).to_bytes(4, 'big')
            # print(img_bytes)
            print(tam_bytes)
            # print(resp)

            # envia a imagem em bytes para o servidor
            self.__tcp.send(img_bytes) 
            print('imagem enviada: ', tam_bytes)

            # recebe a img em bytes
            img_bytes_serv = self.__tcp.recv(65536)
            tam_bytes_serv = len(img_bytes_serv).to_bytes(4, 'big')
            print(img_bytes_serv)
            print('imagem recebida: ', tam_bytes_serv)

            # decodifica a imagem de bytes para o formato original
            img = cv2.imdecode(np.frombuffer(img_bytes_serv, np.uint8), cv2.IMREAD_COLOR)
            print('ok 2')

            # tamanho da imagem em bytes
            # tam_bytes_serv= len(img).to_bytes(4, 'big')

            # tam = int.from_bytes(tam_bytes_serv, 'big')

            if img is None:
                print("Erro: Não foi possível carregar a imagem.")
            else:

                # mostra a imagem processada para o cliente
                cv2.imshow('Imagem Processada', img)
                cv2.waitKey(0)
                cv2.destroyAllWindows()

        except Exception as e:
            print("Erro ao realizar comunicação com o servidor", e.args)

