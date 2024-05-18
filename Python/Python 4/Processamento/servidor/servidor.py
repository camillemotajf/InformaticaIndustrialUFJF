import socket
import cv2
import os
import numpy as np
import threading

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


    def _faceServidor(self, img_bytes):
        """ Define o procedimento a ser feito na imagem pelo servidor"""
        
        # decodificação
        img = cv2.imdecode(np.frombuffer(
            img_bytes, np.uint8), cv2.IMREAD_COLOR)        

        # processamento
        xml_classificador = os.path.join(os.path.relpath(
            cv2.__file__).replace('__init__.py', ''), 'data\haarcascade_frontalface_default.xml')
        face_cascade = cv2.CascadeClassifier(
            xml_classificador)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)

        # codificação da imagem processada
        _, img_bytes_proc = cv2.imencode('.jpg', img)
        img_bytes_proc = bytes(img_bytes_proc)
        tam_bytes_proc = len(img_bytes_proc).to_bytes(4, 'big')

        # mostra a imagem processada
        cv2.imshow('Imagem Processada', img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()  

        return tam_bytes_proc, img_bytes_proc

    def _service(self, con, client):
        print("Atendendo ao Cliente: ", client)
        while True:
            try:

                # recebe a imagem em bytes do cliente
                tam_bytes = con.recv(1024)
                print('tamanho recebido: ', type(tam_bytes))
                tam = int.from_bytes(tam_bytes, 'big')

                # recebe a imagem em bytes do cliente
                img_bytes = con.recv(tam) 
                print('imagem recebida: ', type(img_bytes))

                # procedimento realizado pelo servidor
                tam_bytes_proc, img_bytes_proc = self._faceServidor(img_bytes)

                # envio a imagem processada em bytes para o cliente
                con.send(tam_bytes_proc)
                print("tamanho enviado ", type(tam_bytes_proc))

                con.send(img_bytes_proc)
                print("imagem enviada ", type(img_bytes_proc))
                print(client, "-> requisição atendida")

            except OSError as e:
                print("Erro na conexão ", client, ": ", e.args)
            except Exception as e:
                print("Erro nos dados recebidos pelo cliente ",
                      client, ": ", e.args)
                con.send(bytes("Erro", 'utf-8'))
                return   
            

class ServidorMT(Servidor):
    def __init__(self, host, port):
        """
        Construtor da classe ServidorMT
        """
        super().__init__(host,port)
        self.__threadPool = {} # cria um dicionário para as threads


    def start(self):
        """
        Método que inicializa a execução do servidor
        """
        self.__tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        endpoint = (self._host,self._port)
        try:
            self.__tcp.bind(endpoint)
            self.__tcp.listen(1)
            print("Servidor iniciado em ",self._host,": ", self._port)
            while True:
                con, client = self.__tcp.accept()
                
                # ao invés de criar um serviço dispovível apenas para um cliente, cria threads para aplicar esse serviço
                # concorrentemente
                self.__threadPool[client] = threading.Thread(target=self._service,args=(con,client)) 
                self.__threadPool[client].start()

        except Exception as e:
            print("Erro ao inicializar o servidor",e.args)     