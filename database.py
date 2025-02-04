import json

ARQUIVO_DADOS = "banco_dados.json"

def salvar_dados(central_contas):

    with open(ARQUIVO_DADOS, "w", encoding="utf-8") as arquivo:
        json.dump(central_contas, arquivo, indent=4, ensure_ascii=False)
    print("Dados salvos com sucesso!")

def carregar_dados():
    try:
        with open(ARQUIVO_DADOS, "r", encoding="utf-8") as arquivo:
            return json.load(arquivo)
    except FileNotFoundError:
        print("Nenhum dado encontrado. Criando um novo banco de dados...")
        return {}