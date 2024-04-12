import sqlite3
import time
import datetime
from datetime import date
from genericFunction import *

conn = sqlite3.connect('DBestacionamento.db')
cursor = conn.cursor()

def entraSistema():
    print('=================')
    print('ESCOLHA UMA OPÇÃO')
    print('=================')

    print('1 - ENTRAR COM USUARIO E SENHA')
    print('2 - CADASTRAR USUARIO')

    opcao = int(input("Digite uma opção:"))
    match opcao:
        case 1:
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
                
        case 2:
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
        print('======================')
        print('SISTEMA ESTACIONAMENTO')
        print('======================')

        print('\n1 - REGISTRAR ENTRADA')
        print('2 - REGISTRAR SAÍDA')
        print('3 - LISTAR CARROS ESTACIONADOS')
        print('4 - HISTORICO DE PASSAGENS')
        print('\n')

        opcao = int(input('Digite uma opção: '))
        match opcao:

            case 1: # registra entrada
                limpaCmd()
                print('===================')
                print('REGISTRO DE ENTRADA')
                print('===================')

                placa = str(input('Placa: '))
                modelo = str(input('Modelo: '))
                data_entrada = obtemDataDosistema()

                insertEntrada(placa, modelo, data_entrada)
                limpaCmd()
                msgSucesso(f'\nEntrada da placa {placa} em {data_entrada} cadastrada com sucesso!')

            case 2: # registra saida
                pass
            case 3: # listar carros estacionados
                limpaCmd()
                listarCarrosEstacionados()
                while True:
                    opcao = str(input('\nVoltar [V] || Sair [S]: ')) 
                    if opcao.upper() == "S":
                        msgSucesso('\nPrograma Encerrado!')
                        exit()
                    elif opcao.upper() == "V":
                        limpaCmd()
                        menu()
                    msgErro('\nDigite um valor Válido!')
                

            case 4: # historico de passagens
                pass
            case _:
                limpaCmd()
                msgErro('\nDigite uma opção válida!')

def validaLogin(usuario, senha):
    cursor.execute("""SELECT usuario, senha FROM funcionario WHERE usuario = (?) AND senha = (?)""", (usuario, senha,))
    if len(cursor.fetchall()) == 0:
        return True
 
def insertEntrada(placa, modelo, data_entrada):
    cursor.execute ("""INSERT INTO temp(placa, modelo, data_entrada) 
                VALUES(?,?,?)""",(placa, modelo, data_entrada,))
    conn.commit()

def listarCarrosEstacionados():
    cursor.execute("""SELECT placa, modelo, data_entrada FROM temp""")
    conn.commit()

    print(f"{'Placa' : <20}{'Modelo' : <20}{'Data Entrada' : <20}") 
    for linha in cursor.fetchall():
        print(linha)
    
def obtemDataDosistema():
    date = datetime.datetime.now().strftime("%A %d %B %y %I:%M")
    agora = datetime.datetime.strptime(date, "%A %d %B %y %I:%M")
    return agora
   


menu()