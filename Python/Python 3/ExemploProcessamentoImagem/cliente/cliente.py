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

    def _faceClienteEnviar(self, caminho):

        img = cv2.imread(caminho)

        # codificação para bytes
        _, img_bytes = cv2.imencode('.jpg', img)
        img_bytes = bytes(img_bytes)
        tam_bytes= len(img_bytes).to_bytes(4, 'big')
        
        return tam_bytes, img_bytes
    
    def _faceClienteRecebe(self, img_bytes):

        # decodificação
        img = cv2.imdecode(np.frombuffer(
        img_bytes, np.uint8), cv2.IMREAD_COLOR)

        # mostra a imagem processada pelo servidor
        cv2.imshow('Imagem Processada', img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()       



    def __method(self, caminho):
        try:
            
            tam_bytes, img_bytes = self._faceClienteEnviar(caminho) 
            tam_bytes = bytes(tam_bytes)
            img_bytes = bytes(img_bytes)

            tam = int.from_bytes(tam_bytes, 'big')
            print(tam)

            if img_bytes is None:
                print(f"Error loading image: {caminho}")
            else:
                print("Image loaded successfully")

            # envia a imagem em bytes para o servidor
            self.__tcp.send(tam_bytes) 
            print('tamanho enviado pelo cliente')
            self.__tcp.send(img_bytes)
            print('imagem enviada pelo cliente')

            # recebe o tamnho da imgem em bytes
            tam_bytes_serv = self.__tcp.recv(1024)
            tam_serv = int.from_bytes(tam_bytes_serv, 'big')

            # recebe a imagem processada pelo servidor em bytes
            img_bytes_serv = self.__tcp.recv(tam_serv)

            # mostra a imegem processada pelo servidor
            self._faceClienteRecebe(img_bytes_serv)

            # if img_proc is None:
            #     print("Erro: Não foi possível carregar a imagem.")

        except Exception as e:
            print("Erro ao realizar comunicação com o servidor", e.args)

