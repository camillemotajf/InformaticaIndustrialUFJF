import socket

class Servidor():
    """
    Classe Servidor - API Socket
    """

    def __init__(self, host, port): # cria o objeto socket para comunicação
        """
        Construtor da classe servidor
        """
        self._host = host
        self._port = port
        self.__tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # classe de endereço de comunicação, tipo do socket


    def start(self):
        """
        Método que inicializa a execução do servidor
        """
        endpoint = (self._host, self._port)
        try:
            self.__tcp.bind(endpoint) # atribui o ip e a porta para o serviço
            self.__tcp.listen(1) # espera o cliente -> escuta de clientes -> servidor apto a receber clientes
            print("Servidor iniciado em ", self._host, ": ", self._port)
            while True:
                con, client = self.__tcp.accept() # fica nessa linha até um cliente tentar se comunicar
                self._service(con, client) # serviço disponibilizado pelo servidor
        except Exception as e:
            print("Erro ao inicializar o servidor", e.args)

    def _service(self, con, client):
        """
        Método que implementa o serviço de calculadora
        :param con: objeto socket utilizado para enviar e receber dados
        :param client: é o endereço do cliente
        """
        print("Atendendo cliente ", client)
        while True:
            try:
                msg = con.recv(1024) # recebe a mensagem do cliente em bytes
                msg_s = str(msg.decode('ascii')) # decodificação 
                resp = eval(msg_s) # processamento
                con.send(bytes(str(resp), 'ascii')) # codificação
                print(client, " -> requisição atendida")
            except OSError as e:
                print("Erro de conexão ", client, ": ", e.args)
                return
            except Exception as e:
                print("Erro nos dados recebidos pelo cliente ",
                      client, ": ", e.args)
                con.send(bytes("Erro", 'ascii')) # mensagem de erro enviada ao cliente
                return
