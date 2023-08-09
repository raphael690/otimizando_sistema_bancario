import textwrap
import datetime
# Cores para o Terminal
BLUE = "\033[94m"
RED = "\033[91m"
GREEN = "\033[92m"
CYAN = "\033[96m"
YELLOW = "\033[93m"
PURPLE = "\033[95m"
BOLD =  "\033[1m"
ENDC = "\033[0m"

def menu():
    menu = """\n
    ==================== MENU =======================
    [d]\t{blue}Depositar{end}
    [s]\t{red}Sacar {end}
    [e]\t{green}Extrato{end}    
    [nc]\t{cyan}Nova conta{end}
    [lc]\t{yellow}Listar contas{end}
    [nu]\t{purple}Novo usuáro{end}
    [q]\t{bold}Sair{end}

    =>""".format(blue = BLUE, red = RED, green = GREEN, cyan = CYAN, yellow = YELLOW,
                 purple = PURPLE, bold = BOLD, end = ENDC)

    return input(textwrap.dedent(menu))

def depositar(saldo, valor, extrato, /):
    if valor > 0:
        saldo += valor
        extrato += f"Depósito:\tRS {valor:.2f}\n"
        print("\n=== Depósito realizado com sucesso! ===")
    else:
        print("\n@@@ Operação falhou! O valor informado é inválido. @@@")

    return saldo, extrato    


def sacar(*, saldo, valor, extrato, limite, numero_saques, limite_saques):
    excedeu_saldo = valor > saldo
    excedeu_limite = valor > limite
    excedeu_saques = numero_saques >= limite_saques

    if excedeu_saldo:
        print("\n@@@ Operação falhou! Você não tem saldo suficiente. @@@")
    
    elif excedeu_limite:
        print("\n@@@ Operação falhou! O valor do saque excede o limite. @@@")
    
    elif excedeu_saques:
        print("\n@@@ Operação falhou! Número máximo de saques excedido. @@@")

    elif valor > 0:
        saldo -= valor
        extrato += f"Saque:\t\tR$ {valor:.2f}\n"
        numero_saques += 1
        print("\n === Saque realizado com sucesso! ===")

    else:
        print("\n@@@ Operação falhou! O valor informado é inválido. @@@")

    return saldo, extrato

def exibir_extrato(saldo, /, *, extrato):
    print("\n==============EXTRATO==============")
    print("Não foram realizadas movimentações." if not extrato else extrato)
    print(f"\nSaldo: R$ {saldo:.2f}")
    print("=====================================")


def criar_usuario(usuarios):
    cpf = input("informe o seu CPF (somente número): ")
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print("\n@@ Parece que já existe usuário com esse CPF! @@@")
        return
    
    nome = input("Informe o seu nome completo: ")
    data_nascimento = input("Informe a data do seu nascimento (dd-mm-aaaa): ")
    endereco = input("informe o seu endereço(logradouro, nro - bairro - cidade/sigla estado): ")

    usuarios.append({"nome": nome, "data_nascimento": data_nascimento, "cpf": cpf, "endereco": endereco})

    print("=== Usuário Criado com sucesso! ===")

def filtrar_usuario(cpf, usuarios):
    usuarios_filtrados = [usuario for usuario in usuarios if usuario["cpf"] == cpf]
    return usuarios_filtrados[0] if usuarios_filtrados else None


def criar_conta(agencia, numero_conta, usuarios):
    cpf = input("Informe o CPF do usuário: ")
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print("\n=== Conta criada com sucesso! ===")
        return {"agencia": agencia, "numero_conta": numero_conta, "usuario": usuario}
    
    print("\n@@@ Usuário não encontrado, fluxo de criação de conta encerrado! @@@")


def listar_contas(contas):
    for conta in contas:
        linha = f"""
            Agência:\t\t{conta['agencia']}
            C/C:\t\t{conta['numero_conta']}
            Titular:\t\t{conta['usuario']['nome']}
        """
        print("=" * 100)
        print(textwrap.dedent(linha)) # para formatação do codigo


def main():
    LIMITE_SAQUES = 3
    AGENCIA = "0001"

    saldo = 0
    limite = 500
    extrato = ""
    numero_saques = 0
    usuarios = []
    contas = []
    #numeor_conta = 1

#loop Principal
    while True:
        opcao = menu()
#----- Depósito --------------
        if opcao == "d":
            valor = float(input("Informe o valor do depósito: RS "))

            saldo, extrato = depositar(saldo, valor, extrato)
#------ Saque ----------------
        elif opcao == "s":
            valor = float(input("Informe o valor do saque: RS "))

            saldo, extrato = sacar(
                saldo=saldo,
                valor=valor,
                extrato=extrato,
                limite=limite,
                numero_saques= numero_saques,
                limite_saques=LIMITE_SAQUES,
            )
#------Extrato bancario ----------------
        elif opcao == "e":
            exibir_extrato(saldo, extrato=extrato)
#-------Novo Usuário---------------------
        elif opcao == "nu":
            criar_usuario(usuarios)
#------- Nova Conta ----------------------
        elif opcao == "nc":
            numero_conta = len(contas) + 1
            conta = criar_conta(AGENCIA, numero_conta, usuarios)

            if conta:
                contas.append(conta)
           #    numero_conta += 1
#-------Lista de Contas ------------------
        elif opcao == "lc":
            listar_contas(contas)
#------- Sair ----------------------------
        elif opcao == "q":
            break

        else:
            print("Operação inválida, por fazor selecione novamente a operação desejada.")

main()