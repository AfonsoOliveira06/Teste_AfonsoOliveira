from typing import List
from pydantic import BaseModel

class Movimento(BaseModel):
    descricao: str

class Conta(BaseModel):
    numero_conta: str
    saldo: int
    movimento: List[Movimento] = []

    def depositar(self, valor: int):
        self.saldo += int(valor)
        self.movimento.append(Movimento(descricao=f"Depósito de {valor}"))

    def levantar(self, valor: int):
        if int(valor) < 500:
            if self.saldo >= int(valor):
                self.saldo -= int(valor)
                self.movimento.append(Movimento(descricao=f"Levantamento de {valor}"))
            else:
                raise ValueError("O valor inserido é maior que o saldo da sua conta!")
        else:
            raise ValueError("Não pode levantar mais de 500 euros")

    def consultar_extrato(self):
        return self.movimento

class Banco(BaseModel):
    contas: List[Conta] = []

    def add_conta(self, conta: Conta):
        self.contas.append(conta)

    def transferir(self, num_conta, num_destino, valor: int):
        conta_ori = self.procurar(num_conta)
        conta_dest = self.procurar(num_destino)
        if not conta_ori or not conta_dest:
            raise ValueError("Alguma das contas que inseriu não existe")
        conta_ori.levantar(valor)
        conta_dest.depositar(valor)
        return "Transferência realizada"

    def procurar(self, numero_conta):
        for conta in self.contas:
            if conta.numero_conta == numero_conta:
                return conta
        return None
