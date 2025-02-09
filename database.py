import json

ARQUIVO_DADOS = "banco_dados.json"

def salvar_dados(central_contas):
    with open(ARQUIVO_DADOS, "w", encoding="utf-8") as arquivo:
        json.dump(central_contas, arquivo, indent=4, ensure_ascii=False)
    print("Dados salvos com sucesso!")

def carregar_dados():
    try:
        with open(ARQUIVO_DADOS, "r", encoding="utf-8") as arquivo:
            dados = json.load(arquivo)
            print("Dados carregados com sucesso!")
            return dados
    except FileNotFoundError:
        print("Nenhum dado encontrado. Criando um novo banco de dados...")
        return {}

# Ao inicializar a aplicação, vamos carregar os dados corretamente
central_contas = carregar_dados()
