from datetime import datetime

# Função para localizar uma conta a partir do CPF e número da conta
def encontrar_conta(central_contas, cpf, numero_conta):
    if cpf not in central_contas:
        print("ERRO: Você precisa criar uma conta antes de prosseguir.")
        return None
    
    for conta in central_contas[cpf]["contas"]:
        if conta["numero_conta"] == numero_conta:
            return conta
    
    print("Número de conta inválido")
    return None




# Função para realizar depósitos
def depositar(central_contas, valor_deposito, numero_conta, cpf): 
    conta = encontrar_conta(central_contas, cpf, numero_conta)
    if not conta:
        print("Conta não encontrada")
        return
    
    if valor_deposito <= 0:
        print("ERRO. Valor inválido, tente novamente.")
        return
    
    conta["saldo"] += valor_deposito  # Atualiza o saldo da conta
    data_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    conta["extrato"].append({"data_hora": data_hora, "valor": valor_deposito})  # Registra a transação
    print(f"O seu depósito no valor de R$ {valor_deposito:.2f} foi depositado com sucesso.")

# Função para realizar saques
def sacar(*, central_contas, cpf, numero_conta, valor_saque, limite_saques=3):
    conta = encontrar_conta(central_contas=central_contas, cpf=cpf, numero_conta=numero_conta)
    if not conta:
        print("ERRO: Conta não encontrada.")
        return conta
    
    if conta["numero_saques"] >= limite_saques:
        print("ERRO. Você atingiu o limite de saques por hoje.")
    elif valor_saque > conta["saldo"]:
        print("ERRO. Você não tem saldo suficiente.")
    elif valor_saque > 500:
        print("ERRO. Você só pode sacar 500 reais por vez.")
    elif valor_saque <= 0:
        print("ERRO. Digite um valor válido.")
    else:
        conta["saldo"] -= valor_saque  # Atualiza o saldo
        conta["numero_saques"] += 1  # Atualiza o contador de saques
        print(f"O seu saque no valor de {valor_saque} foi realizado com sucesso!")
    
    data_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    conta["extrato"].append({"data_hora": data_hora, "valor": -valor_saque})  # Registra a transação
    print(f"O seu saque no valor R$ {valor_saque} foi realizado com sucesso.")

    # Função para exibir o extrato da conta
def mostrar_extrato(central_contas, cpf, numero_conta):
    conta = encontrar_conta(central_contas, cpf, numero_conta)
    print(" EXTRATO ".center(40, "="))
    if not conta["extrato"]:
        print("Não há movimentações no seu extrato.")
    else:
        for item in conta["extrato"]:
            tipo = "Depósito" if item["valor"] > 0 else "Saque"
            print(f"{tipo} | Data/Hora: {item['data_hora']} Valor: R$ {item['valor']}")
    print("="*40)
    print(f"Saldo Atual: R$ {conta['saldo']:.2f}")
