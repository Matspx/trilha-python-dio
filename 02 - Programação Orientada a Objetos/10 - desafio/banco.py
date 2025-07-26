from abc import ABC, abstractmethod
from datetime import date, datetime
import pytz
import random 

class PessoaFisica:
    def __init__(self, cpf: str, nome: str, data_de_nascimento: date):
        self._cpf = cpf
        self._nome = nome
        self._data_de_nascimento = data_de_nascimento
        

class Cliente(PessoaFisica):
    def __init__(self, cpf: str, nome: str, data_de_nascimento: date, endereco: str, contas: list):
        super().__init__(cpf, nome, data_de_nascimento)
        self._endereco = endereco
        self._contas = contas
        
    def realizar_transacao(self, conta: "Conta", transacao: "Transacao"):
        transacao.registrar(conta)
    
    def adicionar_conta(self, conta: "Conta"):
        self._contas.append(conta)
        
    def __repr__(self):
        return f"{self._nome, self._contas}"
 
    def __str__(self):
        return self.__repr__()
    
        
class Transacao(ABC):
    @abstractmethod
    def registrar(self, conta: "Conta"):
        pass

class Saque(Transacao):
    def __init__(self, valor: float):
        self._valor = valor

    def registrar(self, conta: "Conta"):
        conta_saque = 0
        data = datetime.now(pytz.timezone('America/Sao_Paulo'))
        data_hoje = data.strftime('%d/%m/%Y')
        for x in conta._historico._transacoes:
            if "Saque" in x and data_hoje in x:
                conta_saque += 1
                
        if conta.sacar(self._valor) and conta._limite_saques > conta_saque:
            print("Saque efetuado com sucesso!")
            conta._historico.adicionar_transacao(self)
        else:
            print("Saque inválido")

    def __repr__(self):
        return f"Saque de R${self._valor:.2f}"
 
    def __str__(self):
        return self.__repr__()
    

class Deposito(Transacao):
    def __init__(self, valor: float):
        self._valor = valor

    def registrar(self, conta: "Conta"):
        if conta.depositar(self._valor):
            print("Depósito efetuado com sucesso!")
            conta._historico.adicionar_transacao(self)
        else:
            print("Depósito inválido")

    def __repr__(self):
        return f"Depósito de R${self._valor:.2f}"
 
    def __str__(self):
        return self.__repr__()
        
class Historico:
    def __init__(self):
        self._transacoes = []

    def transacoes(self):
        return self._transacoes

    def adicionar_transacao(self, transacao: Transacao):
        data = datetime.now(pytz.timezone('America/Sao_Paulo'))
        data_formatada = data.strftime('%d/%m/%Y %H:%M:%S')
        self._transacoes.append(f"{transacao} - {data_formatada}")

    def gerar_relatorio(self, tipo_transacao=None):
        pass

class Conta:
    def __init__(self, saldo: float, numero: int, agencia: str, cliente: Cliente, historico: Historico):
        self._saldo = saldo
        self._numero = numero
        self._agencia = agencia
        self._cliente = cliente
        self._historico = historico
        
    def saldo(self):
        return self._saldo
    
    @classmethod
    def nova_conta(cls, cliente: Cliente, numero: int):  
        agencia = 0
        historico = Historico()
        saldo = 0   
        return cls(saldo, numero, agencia, cliente, historico)
    
    def sacar(self, valor:float):
        if valor > 0 and valor < self._saldo and valor <= self._limite:
            self._saldo -= valor
            return True
        return False
    
    #retornar booleano
    def depositar(self, valor:float):
        if valor > 0:
            self._saldo += valor
            return True
        return False
    
    def __str__(self):
        return f"{self._class.name}: {', '.join([f'{chave}={valor}' for chave, valor in self.dict_.items()])}"

class ContaCorrente(Conta):
    def __init__(self, saldo: float, numero: int, agencia: str, cliente: Cliente, historico: Historico, limite: float, limite_saques: int):
        super().__init__(saldo, numero, agencia, cliente, historico)
        self._limite = limite
        self._limite_saques = limite_saques
        
    @classmethod
    def nova_conta(cls, cliente: Cliente, numero: int):  
        agencia = 1
        historico = Historico()
        saldo = 0
        limite = 500
        limite_saque = 3   
        return cls(saldo, numero, agencia, cliente, historico, limite, limite_saque)
    
    def __repr__(self):
        return f"c/c: {self._numero} - ag: {self._agencia}"
 
    def __str__(self):
        return self.__repr__()

#gerar cliente
pessoa = PessoaFisica('000-000', 'Andre', date(1990,1,1))
cliente = Cliente(pessoa._cpf, pessoa._nome, pessoa._data_de_nascimento, "Rua A", [])

#gerar conta, no momento apenas corrente
conta = ContaCorrente.nova_conta(cliente,1)

#adcionr ao cliente
cliente.adicionar_conta(conta)

#banco de clientes     
db = {f"Admin-{cliente._cpf}": cliente}

def listar_clientes(db):
    for x in db:
        print(db[x])

def menu_acesso(db):
    print(db)
    e_cliente = int(input("Você é cliente?\n[1] Sim\n[2] Não\n[3] Ou você é adiministrador?"))
    cpf = str(input("Digite seu cpf:\n"))
    if e_cliente == 1:
        if db.get(cpf):
            menu_principal(db[cpf])
        else:
            print("CPF não cadastrado\nEfetuar cadastro")
            menu_nova_conta(cpf)
    elif e_cliente == 3:
        if db.get(f"Admin-{cpf}"):
            menu_adiministrador(db[f"Admin-{cpf}"])
        else:
            print("Adiministrador não cadastrado\nTentar novamente")
            menu_acesso(db)
        
    else:
        menu_nova_conta(cpf)

def menu_adiministrador(admin):
    print(F"Bem vindo {cliente._nome}!")
    opcao = ""
    while opcao != "q":
        opcao = input(
            f'''
                [l] listar contas
                [n] Novo usuário
                [q] Sair
            ''')
        if opcao == "l":
            listar_clientes(db)
        if opcao == "n":
            cpf = str(input("Digite seu cpf:\n"))
            menu_nova_conta(cpf)
            
        if opcao == 'q':
            break
         
def menu_principal(cliente):
    conta = cliente._contas[0]
    opcao = ""
    print(F"Bem vindo {cliente._nome}!")
    while opcao != "q":
        opcao = input(
            f'''
                [sa] Saldo
                [d] Despositar
                [s] Sacar
                [e] Extrato
                [q] Sair
            ''')
        
        if opcao == "sa":
            print(f"Saldo: R${conta.saldo():.2f}")
        
        elif opcao == "d":
            valor = float(input("Qual o valor de depósito?\n"))
            deposito = Deposito(valor)
            cliente.realizar_transacao(conta, deposito)  

        elif opcao == "s":
            valor = float(input("Qual o valor de saque?\n"))
            saque = Saque(valor)
            cliente.realizar_transacao(conta, saque) 

        elif opcao == 'e':
            print(conta._historico._transacoes)   

        elif opcao == 'q':
            break
        else:
            print("Opção inválida")      
    
    
def menu_nova_conta(cpf):
    nome = str(input("Digite seu nome:\n"))
    
    dia_de_nascimento = int(input("Digite o dia de nascimento:\n"))
    mes_de_nascimento = int(input("Digite o mes de nascimento:\n"))
    ano_de_nascimento = int(input("Digite o ano de nascimento:\n"))
    
    endereco = str(input("Digite seu endereço:\n"))
    
    pessoa = PessoaFisica(cpf, nome, date(ano_de_nascimento,
                                             mes_de_nascimento,
                                             dia_de_nascimento))
    
    cliente = Cliente(pessoa._cpf, pessoa._nome, pessoa._data_de_nascimento, endereco, [])
    
    numero_conta = ""
    for _ in range(5):
        numero_conta += str(random.randrange(0,9))
        
    conta = ContaCorrente.nova_conta(cliente,int(numero_conta))

    cliente.adicionar_conta(conta)
    
    db[cliente._cpf] = cliente
    menu_acesso(db)

menu_acesso(db)