class Conta:
    def __init__(self,numero_conta:int,saldo:int):
        self.numero_conta = numero_conta
        self.saldo = saldo
        self.movimento = []


    def depositar(self, valor:int):
        self.saldo += int(valor)
        self.movimento.append(f"Depósito de {valor}")


    def levantar(self, valor:int):
        if int(valor) < 500:
            if self.saldo >= int(valor):
                self.saldo -= int(valor)
                self.movimento.append(f"Levantamento de {valor}")

            else:
                return "O valor inserido é maior que o saldo da sua conta!"
        else:
            return "Não pode levantar mais de 500 euros"
    def Consultar_extrato(self):
        return self.movimento

class Banco:
    def __init__(self):
        self.contas = []
    def add_conta(self,conta):
        self.contas.append(conta)

    def transferir(self,num_conta,num_destino,valor:int):
        conta_ori = self.procurar(num_conta)
        conta_dest= self.procurar(num_destino)
        if not conta_ori or not conta_dest:
             return "Alguma das contas que inseriu não existe "
        conta_ori.levantar(valor)
        conta_dest.depositar(valor)
        return "Transeferência realizada"

    def procurar(self,numero_conta):
        for conta in self.contas:
            if conta.numero_conta == numero_conta:
                return conta
        return None


