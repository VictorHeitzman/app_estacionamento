import sqlite3
import datetime
from datetime import date
from tabulate import tabulate
import os
from colorama import init, Fore, Style

conn = sqlite3.connect('DBestacionamento.db')
cursor = conn.cursor()

def entraSistema():
    print('=================')
    print('ESCOLHA UMA OPÇÃO')
    print('=================')

    print('1 - ENTRAR COM USUARIO E SENHA')
    print('2 - CADASTRAR USUARIO')

    opcao = str(input("Digite uma opção:"))
    match opcao:
        case '1':
            while True:
                print("\n")
                usuario = str(input('Login do Usuario: '))
                senha = str(input('Senha do Usuario: '))

                if not(validaLogin(usuario, senha)):
                    limpaCmd()
                    menu()
                    break
                limpaCmd()
                msgErro('Usuario ou Senha Incorretos')
                
        case '2':
            limpaCmd()
            print('===================')
            print('Registro de Usuario')
            print('===================')

            while True:
                usuario = str(input('\nLogin do novo Usuario: '))
                senha = str(input('Senha do novo Usuario: '))
                
                cursor.execute (""" SELECT usuario FROM funcionario 
                    WHERE usuario = (?)""", (usuario,))
                if len(cursor.fetchall()) == 0:
                    cursor.execute (""" INSERT INTO funcionario(usuario, senha) 
                        VALUES (?,?)""", (usuario, senha))
                    conn.commit()
                    
                    limpaCmd()
                    msgSucesso('Usuario Registrado com sucesso')
                    entraSistema()
                    break
                msgErro('Usuario JÃ¡ existente!')

        case _:
            limpaCmd()
            msgErro('Digite apenas 1 ou 2')
            entraSistema()   

def menu():
    while True:
        print('=========================')
        print('SISTEMA DE ESTACIONAMENTO')
        print('=========================')

        print('\n1 - REGISTRAR CLIENTE')
        print('2 - REGISTRAR ENTRADA')
        print('3 - REGISTRAR SAÍDA')
        print('4 - LISTAR CARROS ESTACIONADOS')
        print('5 - LISTAR CLIENTES')
        print('6 - HISTORICO DE PASSAGENS')
        print('\n')

        opcao = str(input('Digite uma opção: '))
        match opcao:

            case '1': # registra Cliente
                print('=================')
                print('REGISTRA CLIENTE')
                print('=================')

                nome = str(input("Nome: "))
                cpf = str(input("CPF: "))
                placa = str(input("placa: ")).upper()
                modelo = str(input("Modelo: ")).upper()

                RegistraCliente(nome, cpf, placa, modelo)
                limpaCmd()
                msgSucesso('Cliente Registrado com sucesso!')
                menu()

            case '2': # registra entrada
                limpaCmd()
                print('===================')
                print('REGISTRO DE ENTRADA')
                print('===================')
                while True:
                    cpf = str(input('cpf: '))
                    if not(verificaSePossuiVeiculo(cpf)):
                        registraEntrada(cpf)
                        menu()
                        break
                    limpaCmd()
                    msgErro('Cpf ou placa não cadastrada')

            case '3': # registra saida
                limpaCmd()
                print('=================')
                print('REGISTRO DE SAÍDA')
                print('=================')

                while True:
                    placa = str(input('Digite a Placa: ')).upper()
                    if validaPlaca(placa):
                        registraSaida(placa)
                    msgErro('Placa não encontrada')

            case '4': # listar carros estacionados
                print('===================')
                print('CARROS ESTACIONADOS')
                print('===================')
                limpaCmd()
                sql = """SELECT c.nome, t.placa, t.modelo, t.data_entrada FROM temp as t
                        INNER JOIN cliente as c
                        on c.placa = t.placa"""
                headers = ['Nome', 'Placa', 'Modelo', 'Data Entrada']

                listarTababela(sql, headers)
            
            case '5': # listar clientes
                print('===================')
                print('CARROS ESTACIONADOS')
                print('===================')
                limpaCmd()

                sql = "SELECT * FROM cliente"
                headers = ['Nome', 'CPF', 'Placa', 'Modelo']
                listarTababela(sql, headers)
            
            case '6': # historico de passagens
                limpaCmd()
                
                sql = "SELECT * FROM historico"
                headers = ['Placa', 'Modelo', 'Data Entrada', 'Data Saída']
                listarTababela(sql, headers)

            case _:
                limpaCmd()
                msgErro('Digite uma opçãoo válida!')

def validaLogin(usuario, senha):
    cursor.execute("""SELECT usuario, senha FROM funcionario WHERE usuario = (?) AND senha = (?)""", (usuario, senha,))
    if len(cursor.fetchall()) == 0:
        return True

def verificaSePossuiVeiculo(cpf):
    cursor.execute("""SELECT placa FROM cliente WHERE cpf = (?)""", (cpf,))
    if (len(cursor.fetchall())) == 0:
        return True

def registraEntrada(cpf):
    
    cursor.execute('SELECT placa, modelo FROM cliente WHERE cpf = (?)', (cpf,))
    valores = cursor.fetchall()
    placa = valores[0][0]
    modelo = valores[0][1]

    cursor.execute('INSERT INTO temp(placa, modelo, data_entrada) VALUES(?,?,?)',(placa, modelo, obtemDataDosistema()))
    conn.commit()

    limpaCmd()
    return msgSucesso(f'Entrada da placa {placa} em {obtemDataDosistema()} cadastrada com sucesso!')
    
def RegistraCliente(nome, cpf, placa, modelo):          
    cursor.execute (f"""INSERT INTO cliente(nome, cpf, placa, modelo) 
                VALUES(?,?,?,?)""",(nome, cpf, placa, modelo,))
    conn.commit()

def listarTababela(sql, headers):
    cursor.execute(sql)
    conn.commit()
    
    print(tabulate(cursor.fetchall(),headers=headers,tablefmt='fancy_grid'))

    while True:
        opcao = str(input('Voltar [V] || Sair [S]: ')) 
        if opcao.upper() == "S":
            limpaCmd()
            msgSucesso('Programa Encerrado!')
            exit()
        elif opcao.upper() == "V":
            limpaCmd()
            menu()
        msgErro('Digite um valor VÃ¡lido!')
 
def validaPlaca(placa):
    cursor.execute("""SELECT placa FROM temp WHERE placa = (?)""", (placa,))
    if len(cursor.fetchall()) == 0:
        return False
    else:
        return True

def registraSaida(placa):
        cursor.execute(f"""DELETE FROM temp WHERE placa = (?)""", (placa,))
        conn.commit()
        limpaCmd()
        msgSucesso('Saída Registrada com Sucesso!')
        menu()


############################################################
# FUNÇÕES GENERICAS
############################################################
def limpaCmd():
    return os.system('cls')

def msgSucesso(msg):
    return print(f'{Fore.GREEN} \n{msg} {Style.RESET_ALL}')   

def msgErro(msg):
    return print(Fore.RED + msg + Style.RESET_ALL)   

def obtemDataDosistema():
    date = datetime.datetime.now().strftime('%d/%m/%Y %H:%M')
    agora = datetime.datetime.strptime(date, '%d/%m/%Y %H:%M')
    return str(agora)

entraSistema()