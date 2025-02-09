import tkinter as tk
from tkinter import ttk  # Importando o ttk para usar o Notebook
from tkinter import messagebox

# Função para criar um novo usuário
def criar_usuario(central_contas, cpf, nome, data_nascimento, cep, bairro, cidade, estado, logradouro, numero_casa):
    """
    Cria um usuário com os dados fornecidos e adiciona ao dicionário central_contas.
    """
    usuario = {
        "cpf": cpf,
        "nome": nome,
        "data_nascimento": data_nascimento,
        "endereco": {
            "cep": cep,
            "bairro": bairro,
            "cidade": cidade,
            "estado": estado,
            "logradouro": logradouro,
            "numero_casa": numero_casa
        },
        "contas": []
    }
    central_contas[cpf] = usuario
    return usuario  # Retorna o usuário criado

# Função para validar CPF
def validar_cpf(cpf):
    """
    Função simples para validar o formato do CPF.
    """
    if len(cpf) != 11 or not cpf.isdigit():
        return False
    return True

# Função para adicionar usuário
def adicionar_usuario():
    """
    Coleta os dados dos campos de entrada e cria um novo usuário no sistema.
    """
    cpf = entry_cpf.get()
    nome = entry_nome.get()
    data_nascimento = entry_data_nascimento.get()
    cep = entry_cep.get()
    bairro = entry_bairro.get()  
    cidade = entry_cidade.get()
    estado = entry_estado.get()
    logradouro = entry_logradouro.get()
    numero_casa = entry_numero_casa.get()

    if not cpf or not nome or not data_nascimento:
        messagebox.showerror("Erro", "Por favor, preencha todos os campos obrigatórios!")
        return
    
    if not validar_cpf(cpf):
        messagebox.showerror("Erro", "CPF inválido. Verifique o formato.")
        return
    
    # Criação do usuário e adição no sistema
    usuario = criar_usuario(central_contas, cpf, nome, data_nascimento, cep, bairro, cidade, estado, logradouro, numero_casa)
    
    # Exibir mensagem de sucesso
    messagebox.showinfo("Sucesso", f"Usuário {nome} criado com sucesso.")
    
    # Limpar campos após a criação do usuário
    limpar_campos_usuario()

# Função para limpar campos do usuário após o cadastro
def limpar_campos_usuario():
    """
    Limpa todos os campos de entrada relacionados ao cadastro de usuário.
    """
    entry_cpf.delete(0, tk.END)
    entry_nome.delete(0, tk.END)
    entry_data_nascimento.delete(0, tk.END)
    entry_cep.delete(0, tk.END)
    entry_bairro.delete(0, tk.END)
    entry_cidade.delete(0, tk.END)
    entry_estado.delete(0, tk.END)
    entry_logradouro.delete(0, tk.END)
    entry_numero_casa.delete(0, tk.END)

# Função para criar uma nova conta
def criar_conta():
    """
    Cria uma nova conta para o usuário com base no CPF fornecido e no tipo de conta.
    """
    cpf = entry_cpf_conta.get()
    tipo_conta = tipo_conta_var.get()

    if not cpf or tipo_conta == "Selecione":
        messagebox.showerror("Erro", "Por favor, preencha todos os campos obrigatórios!")
        return
    
    if cpf not in central_contas:
        messagebox.showerror("Erro", "Usuário não encontrado!")
        return
    
    # Lógica para criar uma nova conta
    central_contas[cpf]['contas'].append(tipo_conta)
    messagebox.showinfo("Sucesso", f"Conta {tipo_conta} criada para o CPF {cpf}.")
    
    # Limpar campos após a criação da conta
    entry_cpf_conta.delete(0, tk.END)
    tipo_conta_var.set("Selecione")

# Função para registrar transação
def registrar_transacao():
    """
    Registra uma transação de depósito ou saque para um usuário, com base nas informações fornecidas.
    """
    cpf = entry_cpf_transacao.get()
    valor = entry_valor_transacao.get()
    tipo_transacao = tipo_transacao_var.get()

    if not cpf or not valor or tipo_transacao == "Selecione":
        messagebox.showerror("Erro", "Por favor, preencha todos os campos obrigatórios!")
        return
    
    if cpf not in central_contas:
        messagebox.showerror("Erro", "Usuário não encontrado!")
        return
    
    try:
        valor = float(valor)
    except ValueError:
        messagebox.showerror("Erro", "Valor inválido. Insira um número válido.")
        return
    
    if tipo_transacao == "Saque" and valor <= 0:
        messagebox.showerror("Erro", "Valor de saque deve ser maior que zero.")
        return
    
    # Lógica para registrar a transação
    messagebox.showinfo("Sucesso", f"Transação {tipo_transacao} de R$ {valor} registrada.")
    
    # Limpar campos após o registro da transação
    limpar_campos_transacao()

# Função para limpar os campos de transação após o registro
def limpar_campos_transacao():
    """
    Limpa os campos de entrada de transação após o registro de uma operação.
    """
    entry_cpf_transacao.delete(0, tk.END)
    entry_valor_transacao.delete(0, tk.END)
    tipo_transacao_var.set("Selecione")

# Função para limpar todos os campos (exemplo para futuras melhorias)
def limpar_todos_campos():
    """
    Limpa todos os campos de entrada de uma vez.
    """
    limpar_campos_usuario()
    limpar_campos_transacao()
    entry_cpf_conta.delete(0, tk.END)
    tipo_conta_var.set("Selecione")

# Configuração inicial da interface
root = tk.Tk()
root.title("Sistema Bancário")

# Central de contas (onde todos os dados dos usuários serão armazenados)
central_contas = {}

# Abas (Notebook)
tab_control = ttk.Notebook(root)

# Aba de criação de usuário
aba_usuarios = tk.Frame(tab_control)
tab_control.add(aba_usuarios, text="Criar Usuário")

# Entradas para criação de usuário
tk.Label(aba_usuarios, text="Nome:").pack(pady=5)
entry_nome = tk.Entry(aba_usuarios)
entry_nome.pack(pady=5)

tk.Label(aba_usuarios, text="Data nascimento (YYYY-MM-DD):").pack(pady=5)
entry_data_nascimento = tk.Entry(aba_usuarios)
entry_data_nascimento.pack(pady=5)

tk.Label(aba_usuarios, text="CPF:").pack(pady=5)
entry_cpf = tk.Entry(aba_usuarios)
entry_cpf.pack(pady=5)

tk.Label(aba_usuarios, text="CEP:").pack(pady=5)
entry_cep = tk.Entry(aba_usuarios)
entry_cep.pack(pady=5)

tk.Label(aba_usuarios, text="Bairro:").pack(pady=5)
entry_bairro = tk.Entry(aba_usuarios)
entry_bairro.pack(pady=5)

tk.Label(aba_usuarios, text="Cidade:").pack(pady=5)
entry_cidade = tk.Entry(aba_usuarios)
entry_cidade.pack(pady=5)

tk.Label(aba_usuarios, text="Estado:").pack(pady=5)
entry_estado = tk.Entry(aba_usuarios)
entry_estado.pack(pady=5)

tk.Label(aba_usuarios, text="Logradouro:").pack(pady=5)
entry_logradouro = tk.Entry(aba_usuarios)
entry_logradouro.pack(pady=5)

tk.Label(aba_usuarios, text="Número da casa:").pack(pady=5)
entry_numero_casa = tk.Entry(aba_usuarios)
entry_numero_casa.pack(pady=5)

# Botão para criar usuário
btn_criar_usuario = tk.Button(aba_usuarios, text="Criar Usuário", command=adicionar_usuario, width=20)
btn_criar_usuario.pack(pady=20)

# Aba de criação de contas
aba_contas = tk.Frame(tab_control)
tab_control.add(aba_contas, text="Criar Conta")

# Entradas para criação de conta
tk.Label(aba_contas, text="CPF:").pack(pady=5)
entry_cpf_conta = tk.Entry(aba_contas)
entry_cpf_conta.pack(pady=5)

tk.Label(aba_contas, text="Tipo de Conta:").pack(pady=5)
tipo_conta_var = tk.StringVar(value="Selecione")
tipo_conta_menu = tk.OptionMenu(aba_contas, tipo_conta_var, "Selecione", "Conta Corrente", "Conta PJ")
tipo_conta_menu.pack(pady=5)

# Botão para criar conta
btn_criar_conta = tk.Button(aba_contas, text="Criar Conta", command=criar_conta, width=20)
btn_criar_conta.pack(pady=20)

# Aba de transações
aba_transacoes = tk.Frame(tab_control)
tab_control.add(aba_transacoes, text="Transações")

# Entradas para transação
tk.Label(aba_transacoes, text="CPF:").pack(pady=5)
entry_cpf_transacao = tk.Entry(aba_transacoes)
entry_cpf_transacao.pack(pady=5)

tk.Label(aba_transacoes, text="Valor:").pack(pady=5)
entry_valor_transacao = tk.Entry(aba_transacoes)
entry_valor_transacao.pack(pady=5)

tk.Label(aba_transacoes, text="Tipo de Transação:").pack(pady=5)
tipo_transacao_var = tk.StringVar(value="Selecione")
tipo_transacao_menu = tk.OptionMenu(aba_transacoes, tipo_transacao_var, "Selecione", "Depósito", "Saque")
tipo_transacao_menu.pack(pady=5)

# Botão para registrar transação
btn_registrar_transacao = tk.Button(aba_transacoes, text="Registrar Transação", command=registrar_transacao, width=20)
btn_registrar_transacao.pack(pady=20)

# Exibindo as abas
tab_control.pack(expand=1, fill="both")

# Iniciando a aplicação
root.mainloop()
