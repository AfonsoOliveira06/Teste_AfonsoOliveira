import sqlite3
from  Classes import Conta
from  Classes import Banco

banco = Banco()

while True:
    print("1 - Criar conta")
    print("2 - Selecionar conta a movimentar")
    print("3 - Levantar dinheiro")
    print("4 - Depositar dinheiro")
    print("5 - Transferir dinheiro entre contas")
    print("6 - Consultar o extrato da conta")
    print("7 - Consultar saldo da conta")
    print("8 - Sair")
    tarefa = input("Insira o numero da atividade que deseja realizar: ")

    if tarefa == "1":
        num_conta = input("Insira o numero que deseja colocar na sua conta: ")
        saldo_inicial = int(input("Insira o saldo incial que quer deixar na conta: "))
        conta = Conta(num_conta, saldo_inicial)
        banco.add_conta(conta)

    elif tarefa == "2":
        num_conta = input("Insira o numero da conta que deseja usar: ")
        conta = banco.procurar(num_conta)
        if not conta:
            print("Conta não encontrada.")
            continue

    elif tarefa == "3":
        aux = int(input("Insira o valor que deseja levantar: "))
        val = conta.levantar(aux)

    elif tarefa == "4":
        aux = int(input("Insira o valor que deseja depositar: "))
        val = conta.depositar(aux)

    elif tarefa == "5":
        num_destino = input("Insira o numero da conta destino: ")
        valor = int(input("Insira o valor a transferir: "))
        conta_destino = banco.procurar(num_destino)
        if not conta_destino:
            print("Conta de destino não encontrada.")
            continue
        banco.transferir(conta.numero_conta, num_destino, valor)


    elif tarefa == "6":
        mov_conta = conta.Consultar_extrato()
        print("Extrato da conta: ")
        for i in mov_conta:
            print(i)

    elif tarefa == "7":
        print(f"Saldo da conta: {conta.saldo}")

    elif tarefa == "8":
        print("Aplicação fechada")
        break

    else:
        print("Opção inválida")






