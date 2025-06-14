from datetime import datetime
import random
import pytz
import json

def carregar_contas():
    with open("db.json", 'r') as file:
        data = json.load(file)
        return data

def criar_conta(contas):
    cpf = str(input('Digite seu cpf: '))
    lista_cpfs = contas.keys()
    if cpf in lista_cpfs:
        print("Cpf já possui um conta")
        user_access(contas)
    else:
        conta = ""
        for x in range(6):
            if x == 4:
                conta += "-"
            else:
                conta += str(random.randint(0,9))
        contas[cpf] = {"conta":conta,
                   "saldo": 0,
                   "extrato": ""
                   }
        with open("db.json", 'w') as file:
            json.dump(contas, file, indent=4)
        print("Conta criada com sucesso")

        user_access(contas)

def user_access(contas):
    print('Acesse sua conta\n')
    cpf = str(input('Digite seu cpf: '))
    conta = str(input('Digite sua conta: '))
    lista_cpfs = contas.keys()
    if cpf in lista_cpfs and contas[cpf]["conta"] == conta:
        print("Acesso efetuado!")
        main(contas, cpf)
    else:
        print("conta incorreta! ")
        opcao = input(
                            '''
                    [a] Tentar novamente
                    [b] Criar conta
                '''
                )
        if opcao == 'a':
            user_access(contas)
        else:
            criar_conta(contas)
                
def main(contas, cpf):
    conta = contas[cpf]
    saldo = conta["saldo"]
    extrato = conta["extrato"]
    limite_saque = 500
    num_saques = 0
    num_depositos = 0
    LIMITES_SAQUES = 3
    LIMITES_OPERACOES = 10
    while True:
        opcao = input(
        '''
            [d] Despositar
            [s] Sacar
            [e] Extrato
            [q] Sair
        
        '''
        )
        if opcao == 'd':
            valor_deposito = int(input("qual o valor de depósito?"))
            saldo, extrato, num_depositos = deposito(saldo, valor_deposito, extrato, num_depositos, num_saques, LIMITES_OPERACOES)
            
        elif opcao == 's':
            valor_saque = int(input("qual o valor de saque?"))
            saldo, extrato, num_saques = saque(
                saldo=saldo, 
                valor=valor_saque,
                extrato=extrato,
                limite=limite_saque,
                num_saques=num_saques,
                num_depositos = num_depositos,
                operacoes=LIMITES_OPERACOES,
                limite_saque=LIMITES_SAQUES
                )
            
        elif opcao == 'e':
            gerar_extrato(saldo, extrato=extrato)
                        
        elif opcao == 'q':
            contas[cpf]["saldo"] = saldo
            contas[cpf]["extrato"] = extrato
            with open("db.json",'w') as file:
                json.dump(contas, file, indent=4)
            break
        
        else:
            print('opção inválida, escolha outra')

def deposito(saldo, valor, extrato, num_depositos,num_saques, operacoes, /):
    
    if operacoes <= num_depositos + num_saques:
        print('Limite de transações atingido')
        return

    data = datetime.now(pytz.timezone('America/Sao_Paulo'))
    extrato += (f'Depósito: ${valor:.2f} - {data} \n')
    print(f'Depósito: {valor} \n')
    
    num_depositos += 1
    
    saldo += valor  
    
    return saldo, extrato, num_depositos

def saque(*, saldo, valor, extrato, limite, num_saques, num_depositos, operacoes, limite_saque):
    
    if(num_saques < limite_saque):
        
        if valor > limite:
            print('valor de saque acima do permitido')
            return
        
        elif valor > saldo:
            print('Não será possivel o saque por falta de saldo')
            return
        
        elif operacoes <= num_depositos + num_saques:
            print('Limite de transações atingido')
            return
        
        data = datetime.now(pytz.timezone('America/Sao_Paulo'))
        
        extrato += (f'Saque: ${valor:.2f} - {data}\n')
        print(f'Saque: {valor} \n')  
        
        num_saques += 1
        saldo -= valor
        return saldo, extrato, num_saques
    else:
        print("número limite de saques diário atingido")
        
def gerar_extrato(saldo,/,*,extrato):
    print("\n========= Extrato =========")
    print("Sem movimentações" if not extrato else extrato)
    print(f"seu saldo é de ${saldo:.2f}")
    print("\n===========================")

user_access(carregar_contas())
#criar_conta(carregar_contas())
