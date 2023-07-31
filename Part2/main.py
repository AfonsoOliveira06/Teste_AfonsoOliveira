from fastapi import FastAPI
from Classes import Movimento, Conta, Banco
import sqlite3

app = FastAPI()

banco = Banco()  # Criando uma instância do banco para armazenar as contas


@app.get("/")
async def root():
    return {"message": "Bem-vindo"}


@app.post("/criar_conta")
async def criar_conta(conta: Conta):
    conn = sqlite3.connect("Banco.sqlite")
    conn.execute(f""" 
        insert into contas ("numero_conta", "saldo")
                                  values ("{conta.numero_conta}", {conta.saldo})
    """)
    conn.commit()
    conn.close()
    return {"message": "Conta criada com sucesso!"}

@app.post("/depositar/{numero_conta}/{valor}")
async def depositar(numero_conta: int, valor: int):
    conn = sqlite3.connect("Banco.sqlite")
    cursor = conn.cursor()

    cursor.execute(f"""
            SELECT numero_conta, saldo FROM contas WHERE numero_conta = ?
        """, (numero_conta,))

    result = cursor.fetchone()
    if result:
        numero_conta, saldo = result
        add = saldo + valor
        conn = sqlite3.connect("Banco.sqlite")
        cursor = conn.cursor()

        cursor.execute(f""" 
                UPDATE contas SET saldo = ? WHERE numero_conta = ?
        """, (add, numero_conta))

        conn.commit()
        conn.close()
    return {"error": "Essa conta não existe"}


@app.post("/levantar/{numero_conta}/{valor}")
async def levantar(numero_conta: int, valor: int):
    if valor > 500:
        return {"error":"Não pode levantar valores acima de 500"}
    else:
        conn = sqlite3.connect("Banco.sqlite")
        cursor = conn.cursor()

        cursor.execute(f"""
                    SELECT numero_conta, saldo FROM contas WHERE numero_conta = ?
                """, (numero_conta,))

        result = cursor.fetchone()
        if result:
            numero_conta, saldo = result
            add = saldo - valor
            conn = sqlite3.connect("Banco.sqlite")
            cursor = conn.cursor()

            cursor.execute(f""" 
                        UPDATE contas SET saldo = ? WHERE numero_conta = ?
                """, (add, numero_conta))

            conn.commit()
            conn.close()
        return {"error": "Essa conta não existe"}


@app.get("/saldo/{numero_conta}")
async def consultar_saldo(numero_conta: str):
    conn = sqlite3.connect("Banco.sqlite")
    cursor = conn.cursor()

    cursor.execute(f""" 
        SELECT numero_conta, saldo FROM contas WHERE numero_conta = ?
    """, (numero_conta,))

    result = cursor.fetchone()
    conn.close()
    numero_conta, saldo = result
    return f"numero_conta {numero_conta}, saldo {saldo}"
