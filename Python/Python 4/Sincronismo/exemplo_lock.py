import threading
import time


class ContaBancaria:
    """
    Quando o lock é utilizado, há a sincronização entre as threads do método disparar_ordens
    Quando ele não é utilizado, há uma condição de corrida que deixa o comportamento do sistema inconsistente
    """

    def __init__(self, saldo_inicial):
        self.saldo = saldo_inicial
        self.lock = threading.Lock() # cria um objeto lock que auxilia no compartilhamento de compartilhamento de recursos

    def transferirTheads(self, valor):
        # with self.lock:
        self.lock.acquire() # bloqueia o recurso compartilhado - cria a seção crítica
        saldo_atual = self.saldo
        time.sleep(0.1)
        saldo_atual -= valor
        time.sleep(0.1)
        self.saldo = saldo_atual
        print(f'Transferência realizada: {valor} | Saldo atual: {self.saldo}')
        self.lock.release() # desbloqueia o recurso para a próxima thead

    def transferir(self, valor):
        saldo_atual = self.saldo
        time.sleep(0.1)
        saldo_atual -= valor
        time.sleep(0.1)
        self.saldo = saldo_atual
        print(f'Transferência realizada: {valor} | Saldo atual: {self.saldo}')

        
    def disparar_ordensTheads(self, ordens):
        thread_pool = []
        for ordem in ordens:
            thread_pool.append(threading.Thread(
                target=conta.transferirTheads, args=(ordem,)))
            thread_pool[-1].start() # executa a ultima thread
        for th in thread_pool:
            th.join() # espera terminar todas as threads para terminar o programa 

    def disparar_ordens(self, ordens):
        thread_pool = []
        for ordem in ordens:
            thread_pool.append(threading.Thread(
                target=conta.transferir, args=(ordem,)))
            thread_pool[-1].start() # executa a ultima thread
        for th in thread_pool:
            th.join() # espera terminar todas as threads para terminar o programa 

saldo_inicial = 200

conta = ContaBancaria(saldo_inicial)

ordens_para_transferencia = [50, 70, 20, 60]

conta.disparar_ordens(ordens_para_transferencia)

print(f'Saldo final: {conta.saldo}')

saldo_inicial = 200

conta = ContaBancaria(saldo_inicial)

ordens_para_transferencia = [50, 70, 20, 60]

conta.disparar_ordensTheads(ordens_para_transferencia)

print(f'Saldo final: {conta.saldo}')