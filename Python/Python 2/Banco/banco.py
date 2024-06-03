from contas import Conta

class Banco():
    contas = []
    senhaF = 5658
    def __init__(self):
        self.contas.append(Conta(numero=1,titular="João", senha= 1234, saldoi=300))

        for contas in self.contas:
            print(contas.numero)
    
    def numeroContas(self):
        return len(self.contas)
    
    def exibeContas(self):
        for conta in self.contas:
            print(f"Titular: {conta.titular} | Número: {conta.numero}")

    def buscarConta(self, numero):
        for conta in self.contas:
            if conta.numero == numero:
                return conta
            
    def setSenhaFun(self, senha_nova):
        self.senhaF = senha_nova

    def cadastroCliente(self):
        titular = input("Digite o nome do titular da nova conta: ")
        senha = int(input("Digite a senha para a nova conta: "))
        saldo = float(input("Digite o saldo inicial da conta: "))
        num = self.numeroContas() + 1
        self.contas.append(Conta(numero=num, titular=titular, senha=senha,saldoi=saldo))
            
    def atendimento(self):

        atendimento = True
        print("Bem-vindo ao sistema de atendimento do Banco")
        id = int(input("Digite 1 para funcionário ou 2 para cliente: "))

        if id == 2:
            num = int(input("Digite o número da sua conta: "))

            conta_cliente = self.buscarConta(num)

            if conta_cliente == -1:
                print("Conta Inválida")
            else:
                senha_cliente = int(input("Digite a senha: "))
                if not conta_cliente.validarSenha(senha_cliente):
                    print("Senha Inválida!")
                else:
                    while atendimento:
                        op = int(input(print("Qual operação deseja fazer? (1 - Saque, 2 - Deposito, 3 - Ver Saldo, 4 - Sair): ")))
                        if op == 1:
                            valor = float(input("Digite o valor: "))
                            conta_cliente.saque(senha_cliente, valor)
                        elif op == 2:
                            valor = float(input("Digite o valor: "))
                            conta_cliente.deposito(valor)
                        elif op == 3: 
                            print("Saldo: R$ ", conta_cliente.getSaldo(senha_cliente))
                        elif op == 4:
                            atendimento = False

        elif id == 1:
            senha_funcionario = int(input("Digite a senha do funcionário: "))

            if senha_funcionario == self.senhaF: 
                while atendimento:
                    op = int(input(print("Qual operação deseja fazer? (1 - Mudança de Senha, 2 - Cadastro de Cliente, 3 - Ver Contas Cadastradas, 4 - Sair): ")))
                    if op == 1:
                        new_senha = float(input("Digite a nova senha: "))
                        self.setSenhaFun(new_senha)
                    elif op == 2:
                        self.cadastroCliente()
                    elif op == 3:
                        self.exibeContas()
                    elif op == 4:
                        atendimento = False
                        



            
