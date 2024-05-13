import socket
import cv2
import numpy as np

class Cliente():
    def __init__(self, server_ip, port):
        self.__server_ip = server_ip
        self.__port = port
        self.__tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def start(self):
        endpoint = (self.__server_ip, self.__port)
        try:
            self.__tcp.connect(endpoint)
            print("Conexão Realizada com Sucesso!")
            self.__method()
        except:
            print('Servidor não disponível')

    def __method(self):
        try:
            caminho = ''
            while True:
                caminho = input("Digite o caminho da imagem a ser processada (x para sair): ")
                if caminho == '':
                    continue
                elif caminho == 'x':
                    break
                # envia o caminho em bytes
                print(type(caminho))
                caminho_cod = bytes(caminho, 'ascii')
                print(type(caminho_cod))
                self.__tcp.send(caminho_cod) 
                print('ok')

                # recebe uma tupla em bytes -> (img, tam)
                resp = self.__tcp.recv(4096)

                img_bytes = resp[0].to_bytes(len(str(resp[0])), 'big') # Decodifica os bytes para string
                tam_bytes = resp[1].to_bytes(len(str(resp[1])), 'big') # Decodifica os bytes para string
                print('ok 2', img_bytes, tam_bytes)

                # decodifica a imagem de bytes para formato original
                tam = int.from_bytes(tam_bytes, 'big')
                print('ok 3')
                img = cv2.imdecode(np.frombuffer(img_bytes, np.uint8), cv2.IMREAD_COLOR)
                print('ok 4')

                if img is None:
                    print("Erro: Não foi possível carregar a imagem.")
                else:
                    cv2.imshow('Imagem', img)
                    cv2.waitKey(0)
                    cv2.destroyAllWindows()
                
                # # mostra a imagem processada na tela
                # cv2.imshow('Imagem Processada', img)
                # cv2.waitKey(0) 

        except Exception as e:
            print("Erro ao realizar comunicação com o servidor", e.args)

