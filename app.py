import sqlite3
import time
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
                msgErro('\nUsuario ou Senha Incorretos')
                
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
                    msgSucesso('\nUsuario Registrado com sucesso')
                    entraSistema()
                    break
                msgErro('Usuario Já existente!')

        case _:
            limpaCmd()
            msgErro('\nDigite apenas 1 ou 2')
            entraSistema()   

def menu():
    while True:
        print('=========================')
        print('SISTEMA DE ESTACIONAMENTO')
        print('=========================')

        print('\n1 - REGISTRAR ENTRADA')
        print('2 - REGISTRAR SAÍDA')
        print('3 - LISTAR CARROS ESTACIONADOS')
        print('4 - HISTORICO DE PASSAGENS')
        print('\n')

        opcao = str(input('Digite uma opção: '))
        match opcao:

            case '1': # registra entrada
                limpaCmd()
                print('===================')
                print('REGISTRO DE ENTRADA')
                print('===================')

                placa = str(input('Placa: ')).upper()
                modelo = str(input('Modelo: ')).upper()
                data_entrada = obtemDataDosistema()

                registraEntrada(placa, modelo, data_entrada)
                limpaCmd()
                msgSucesso(f'\nEntrada da placa {placa} em {data_entrada} cadastrada com sucesso!')
                menu()

            case '2': # registra saida
                limpaCmd()
                print('=================')
                print('REGISTRO DE SAÍDA')
                print('=================')

                while True:
                    placa = str(input('Digite a Placa: ')).upper()
                    if validaPlaca(placa):
                        registraSaida(placa)
                    msgErro('\nPlaca não encontrada')

            case '3': # listar carros estacionados
                print('===================')
                print('CARROS ESTACIONADOS')
                print('===================')
                limpaCmd()
                listarCarrosEstacionados('temp')
                
            case '4': # historico de passagens
                limpaCmd()
                listarCarrosEstacionados('historico')

            case _:
                limpaCmd()
                msgErro('\nDigite uma opção válida!')

def validaLogin(usuario, senha):
    cursor.execute("""SELECT usuario, senha FROM funcionario WHERE usuario = (?) AND senha = (?)""", (usuario, senha,))
    if len(cursor.fetchall()) == 0:
        return True
 
def registraEntrada(placa, modelo, data_entrada):
    cursor.execute ("""INSERT INTO temp(placa, modelo, data_entrada) 
                VALUES(?,?,?)""",(placa, modelo, data_entrada,))
    conn.commit()

def listarCarrosEstacionados(tabela):
    cursor.execute(f"""SELECT * FROM {tabela}""")
    conn.commit()
    
    headers = ['Placa', 'Modelo', 'Data Entrada'] if tabela == 'temp' else ['Placa', 'Modelo', 'Data Entrada', 'Data Saída']
    
    print(tabulate(cursor.fetchall(),headers=headers,tablefmt='fancy_grid'))

    while True:
        opcao = str(input('\nVoltar [V] || Sair [S]: ')) 
        if opcao.upper() == "S":
            limpaCmd()
            msgSucesso('\nPrograma Encerrado!')
            exit()
        elif opcao.upper() == "V":
            limpaCmd()
            menu()
        msgErro('\nDigite um valor Válido!')
 
def obtemDataDosistema():
    date = datetime.datetime.now().strftime('%d/%m/%Y %H:%M')
    agora = datetime.datetime.strptime(date, '%d/%m/%Y %H:%M')
    return agora

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
        msgSucesso('\nSaída Registrada com Sucesso!')
        menu()

def limpaCmd():
    return os.system('cls')

def msgSucesso(msg):
    return print(Fore.GREEN + msg + Style.RESET_ALL)   

def msgErro(msg):
    return print(Fore.RED + msg + Style.RESET_ALL)   

print(obtemDataDosistema())