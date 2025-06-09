menu = '''
[d] Despositar
[s] Sacar
[e] Extrato
[q] Sair
 
'''
saldo = 0
limite = 500
extrato = ""
num_saques = 0
LIMITES_SAQUES = 3

def soma_valores(valor_deposito):
    global saldo,extrato
    saldo += valor_deposito
    
    print(f'Depósito: {valor_deposito}')
    extrato += f'Depósito: ${valor_deposito:.2f}\n'
    
    return saldo

def saque_valores(valor_saque):
    global saldo, extrato, LIMITES_SAQUES, num_saques
    if(num_saques < LIMITES_SAQUES):
        
        if valor_saque > 500:
            print('valor inválido')
            return
        
        elif valor_saque > saldo:
            print('Não será possivel o saque por falta de saldo')
            return
            
        saldo -= valor_saque
        print(f'Saque: {valor_saque} \n')  
        extrato += f'Saque: ${valor_saque:.2f}\n'
        
        num_saques += 1
        return saldo
    else:
        print("número limite de saques diário atingido")

while True:
    opcao = input(menu)
    
    if opcao == 'd':
        valor_deposito = int(input("qual o valor de depósito?"))
        soma_valores(valor_deposito)
        
    elif opcao == 's':
        valor_saque = int(input("qual o valor de saque?"))
        saque_valores(valor_saque)
         
    elif opcao == 'e':
        print("\n========= Extrato =========")
        print("Sem movimentações" if not extrato else extrato)
        print(f"seu saldo é de ${saldo:.2f}")
        print("\n===========================")
                    
    elif opcao == 'q':
        break
    
    else:
        print('opção inválida, escolha outra')
