from endereco import criar_endereco

# Função para criar um novo usuário no sistema bancário
def criar_usuario(central_contas, cpf, nome, data_nascimento, cep, bairro, cidade, estado, logradouro, numero_casa):
    if cpf in central_contas:
        print("Esse CPF já está vinculado ao banco. Tente fazer login!")
        return None  # Ou você pode optar por lançar uma exceção
    else:
        # Criando o endereço chamando a função do outro arquivo
        endereco = criar_endereco(cep, bairro, cidade, estado, logradouro, numero_casa)

        # Armazena os dados do usuário e uma lista para suas contas
        central_contas[cpf] = {
            "nome": nome,
            "data_nascimento": data_nascimento,
            "endereco": endereco,
            "contas": []
        }
    print(f"Usuário {nome} criado com sucesso.")
    return central_contas[cpf]  # Retorna o usuário recém-criado
