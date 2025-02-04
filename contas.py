def criar_conta_corrente(central_contas, cpf, tipo_conta, cnpj=None):
    if cpf not in central_contas:
        print("CPF não encontrado. Primeiro crie um usuário.")
        return None
    
    agencia = "0001"  # Número da agência é fixo

    if tipo_conta == "PJ" and not cnpj:
        print("ERRO: Um CNPJ válido é necessário para a criação da conta PJ.")
        return
    
    # Número da conta é sequencial para o usuário
    numero_conta = len(central_contas[cpf]["contas"]) + 1

    # Criação do dicionário que representa a conta
    nova_conta = {
        "agencia": agencia,
        "numero_conta": numero_conta,
        "tipo_conta": tipo_conta,
        "saldo": 0,  # Saldo inicial da conta
        "extrato": [],  # Lista para armazenar transações
        "numero_saques": 0  # Contador de saques diários
    }
    
    if tipo_conta == 'PJ':
        nova_conta["cnpj"] = cnpj
    
    # Adiciona a conta na lista de contas do usuário
    central_contas[cpf]["contas"].append(nova_conta)

    print(f"Conta {tipo_conta} foi criada para o CPF {cpf} com o número da conta {numero_conta}")
    if tipo_conta == "PJ":
        print(f"CNPJ vinculado: {cnpj}")
    
    return numero_conta  # Retorna o número da conta criada