from flask import Flask, render_template, redirect, request
from classes import Conta, Banco
import sqlite3
app = Flask(__name__)


@app.route('/')
def hello_world():
    return render_template('index.html',
                           header="Banco",
                           )


@app.route("/criar_conta", methods=["POST"])
def criar_conta():
    numero_conta = request.form['numero_conta']
    saldo = request.form['saldo']
    conn = sqlite3.connect("Banco_Part3.sqlite")
    conn.execute(f""" 
            insert into contas ("numero_conta", "saldo")
                                      values ("{numero_conta}", {saldo})
        """)
    conn.commit()
    conn.close()
    return redirect("/")


@app.route('/levantar', methods=['POST'])
def levantar():
    numero_conta = request.form['num_conta']
    valor = request.form['valor']
    if int(valor) > 500:
        return {"error": "Não pode levantar valores acima de 500"}
    else:
        conn = sqlite3.connect("Banco_Part3.sqlite")
        cursor = conn.cursor()

        cursor.execute(f"""
                    SELECT numero_conta, saldo FROM contas WHERE numero_conta = ?
                """, (numero_conta,))

        result = cursor.fetchone()
        if result:
            numero_conta, saldo = result
            add = saldo - int(valor)
            conn = sqlite3.connect("Banco_Part3.sqlite")
            cursor = conn.cursor()

            cursor.execute(f""" 
                        UPDATE contas SET saldo = ? WHERE numero_conta = ?
                """, (add, numero_conta))

            cursor.execute(f"""
                                           insert into movimentos ("numero_conta","descricao", "valor")
                                                      values ("{numero_conta}","{f"Depósito de {valor}"}", {valor})
                        """)

            conn.commit()
            conn.close()
        else:
            return {"error": "Essa conta não existe"}
        return redirect('/')

@app.route('/depositar', methods=['POST'])
def depositar():
        numero_conta = request.form['num_conta']
        valor = request.form['valor']
        conn = sqlite3.connect("Banco_Part3.sqlite")
        cursor = conn.cursor()

        cursor.execute(f"""
                SELECT numero_conta, saldo FROM contas WHERE numero_conta = ?
            """, (numero_conta,))

        result = cursor.fetchone()
        if result:
            numero_conta, saldo = result
            add = saldo + int(valor)
            conn = sqlite3.connect("Banco_Part3.sqlite")
            cursor = conn.cursor()

            cursor.execute(f""" 
                    UPDATE contas SET saldo = ? WHERE numero_conta = ?
            """, (add, numero_conta))

            cursor.execute(f"""
                                   insert into movimentos ("numero_conta","descricao", "valor")
                                              values ("{numero_conta}","{f"Levantamento de {valor}"}", {valor})
                """)
            conn.commit()
            conn.close()
        else:
            return {"error": "Essa conta não existe"}
        return redirect('/')

@app.route('/consultar_extratos', methods=['POST'])
def consultar_extratos():
    num_conta = request.form['num_conta']
    conn = sqlite3.connect('Banco_Part3.sqlite')
    cursor = conn.cursor()
    cursor.execute(f"""
    SELECT descricao FROM movimentos WHERE numero_conta = ?
            """, (num_conta,))
    movimentos = cursor.fetchall()
    conn.close()
    return render_template('index.html', movimentos=movimentos)

@app.route('/ver_saldo', methods=['POST'])
def ver_saldo():
    num_conta = request.form['num_conta']
    conn = sqlite3.connect('Banco_Part3.sqlite')
    cursor = conn.cursor()
    cursor.execute(f"""
    SELECT saldo FROM contas WHERE numero_conta = ?
    """, (num_conta,))
    saldo = cursor.fetchone()
    conn.close()
    if saldo:
        saldo = saldo
    else:
        return "Erro: A conta não existe."
    return render_template('index.html', saldo=saldo)

@app.route('/transferir', methods=['POST'])
def transferir():
    num_conta = request.form['num_conta']
    num_destino = request.form['num_destino']
    valor = int(request.form['valor'])

    conn = sqlite3.connect('Banco_Part3.sqlite')
    cursor = conn.cursor()

    cursor.execute(f"""
        SELECT numero_conta FROM contas WHERE numero_conta IN (?, ?)
    """, (num_conta, num_destino))
    result = cursor.fetchall()
    if len(result) < 2:
        conn.close()
        return {"error": "Uma ou ambas as contas não existem."}

    cursor.execute(f"""
        SELECT saldo FROM contas WHERE numero_conta = ?
    """, (num_conta,))
    saldo_conta_origem = cursor.fetchone()[0]

    if saldo_conta_origem < valor:
        conn.close()
        return {"error": "Saldo insuficiente para realizar a transferência."}

    cursor.execute(f"""
        UPDATE contas SET saldo = saldo - ? WHERE numero_conta = ?
    """, (valor, num_conta))

    cursor.execute(f"""
        UPDATE contas SET saldo = saldo + ? WHERE numero_conta = ?
    """, (valor, num_destino))

    cursor.execute(f""" 
        INSERT INTO movimentos (numero_conta, descricao, valor)
        VALUES (?, ?, ?)
    """, (num_conta, f"Transferência para a conta {num_destino}", -valor))

    cursor.execute(f""" 
        INSERT INTO movimentos (numero_conta, descricao, valor)
        VALUES (?, ?, ?)
    """, (num_destino, f"Transferência da conta {num_conta}", valor))

    conn.commit()
    conn.close()

    return redirect('/')


if __name__ == '__main__':
    app.run()