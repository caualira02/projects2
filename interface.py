import tkinter as tk
from tkinter import messagebox
from usuarios import criar_usuario
from database import salvar_dados, carregar_dados
from contas import criar_conta_corrente

# Carrega os dados ao iniciar
central_contas = carregar_dados()



# Criando a janela principal
janela = tk.Tk()
janela.title("Sistema Bancário")
janela.geometry("600x500")

# Criando frames para alternar entre as janelas
aba_usuarios = tk.Frame(janela)
aba_contas = tk.Frame(janela)
aba_listar_contas = tk.Frame(janela)
aba_transacoes = tk.Frame(janela)
aba_extrato = tk.Frame(janela)


# Função para alternar entre as abas
def mostrar_aba(aba):
    for frame in [aba_usuarios, aba_contas, aba_listar_contas, aba_transacoes, aba_extrato]:
        frame.pack_forget()
    aba.pack()

# ------- ABA DE CRIAÇÃO DE USUÁRIOS -------

# Criar novo usuário
def adicionar_usuario():
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
    
    criar_usuario(central_contas, cpf, nome, data_nascimento, cep, bairro, cidade, estado, logradouro, numero_casa)
    
    # Salva os dados após criar um usuário
    salvar_dados(central_contas) 
    messagebox.showinfo("Sucesso", f"Usuário {nome} criado com sucesso.")
    
    # Limpa os campos
    entry_cpf.delete(0, tk.END)
    entry_nome.delete(0, tk.END)
    entry_data_nascimento.delete(0, tk.END)
    entry_cep.delete(0, tk.END)
    entry_bairro.delete(0, tk.END)
    entry_cidade.delete(0, tk.END)
    entry_estado.delete(0, tk.END)
    entry_logradouro.delete(0, tk.END)
    entry_numero_casa.delete(0, tk.END)

# Adicionando o campo CPF 
tk.Label(janela, text="CPF:").pack()
entry_cpf = tk.Entry(janela)
entry_cpf.pack()

tk.Label(janela, text="Nome:").pack()
entry_nome = tk.Entry(janela)
entry_nome.pack()

tk.Label(janela, text="Data nascimento (YYYY-MM-DD):").pack()
entry_data_nascimento = tk.Entry(janela)
entry_data_nascimento.pack()

tk.Label(janela, text="CEP:").pack()
entry_cep = tk.Entry(janela)
entry_cep.pack()

tk.Label(janela, text="Bairro:").pack()
entry_bairro = tk.Entry(janela)
entry_bairro.pack()

tk.Label(janela, text="Cidade:").pack()
entry_cidade = tk.Entry(janela)
entry_cidade.pack()

tk.Label(janela, text="Estado:").pack()
entry_estado = tk.Entry(janela)
entry_estado.pack()

tk.Label(janela, text="Logradouro:").pack()
entry_logradouro = tk.Entry(janela)
entry_logradouro.pack()

tk.Label(janela, text="Número da Casa:").pack()
entry_numero_casa = tk.Entry(janela)
entry_numero_casa.pack()


# ------- ABA DE CRIAÇÃO DE CONTAS -------

def adicionar_conta():
    cpf = entry_cpf_conta.get()
    tipo_conta = tipo_conta_var.get()

    if not cpf or tipo_conta not in["PF", "PJ"]:
        messagebox.showerror("Erro", "Preencha todos os campos corretamente.")
        return
    
    # Caso seja PJ, exigir o CNPJ
    cnpj = entry_cnpj.get() if tipo_conta == "PJ" else None

    if tipo_conta == "PJ" and not cnpj:
        print("Erro", "Uma conta PJ, necessita de um CNPJ")
        return
    
    # Criar conta bancaria
    numero_conta = criar_conta_corrente(central_contas, cpf, tipo_conta, cnpj=cnpj)

    if numero_conta:
        salvar_dados(central_contas)
        messagebox.showinfo("Sucesso", f"Conta {tipo_conta} criada para o CPF {cpf}, número de conta {numero_conta}")

    # Limpa os campos
    entry_cpf_conta.delete(0, tk.END)
    if tipo_conta == 'PJ':
        entry_cnpj.delete(0, tk.END)

# Criando os campos de entrada para a criação de conta
tk.Label(aba_contas, text="CPF do Titular:").pack()
entry_cpf_conta = tk.Entry(aba_contas)
entry_cpf_conta.pack()

tk.Label(aba_contas, text="Tipo de Conta:").pack()
tipo_conta_var = tk.StringVar()
tipo_conta_var.set("PF") # Valor padrão

tk.Radiobutton(aba_contas, text="Pessoa Física (PF)", variable=tipo_conta_var, value="PF").pack()
tk.Radiobutton(aba_contas, text="Pessoa Jurídica (PJ)", variable=tipo_conta_var, value="PJ").pack()

# Campo opcional para CNPJ (só para PJ)
tk.Label(aba_contas, text="CNPJ (somente para PJ):").pack()
entry_cnpj = tk.Entry(aba_contas)
entry_cnpj.pack()


# Exibe a aba inicial
mostrar_aba(aba_usuarios)

# ------- ABA DE LISTAGEM DE CONTAS -------
def listar_contas():
    cpf = entry_cpf_listar.get()
    
    if cpf not in central_contas:
        messagebox.showerror("Erro", "CPF não encontrado!")
        return
    
    contas = central_contas[cpf]["contas"]
    
    if not contas:
        messagebox.showinfo("Aviso", "Nenhuma conta encontrada para este usuário.")
        return
    
    resultado = "\n".join([f"Conta {conta['tipo']}: {conta['numero_conta']}" for conta in contas])
    messagebox.showinfo("Contas do Usuário", resultado)

aba_listar_contas = tk.Frame(janela)

tk.Label(aba_listar_contas, text="CPF do Usuário:").pack()
entry_cpf_listar = tk.Entry(aba_listar_contas)
entry_cpf_listar.pack()


# ------- ABA DE TRANSAÇÕES -------
def realizar_transacao():
    tipo = tipo_transacao_var.get()
    cpf = entry_cpf_transacao.get()
    numero_conta = entry_numero_conta.get()
    valor = float(entry_valor.get())
    
    if cpf not in central_contas:
        messagebox.showerror("Erro", "CPF não encontrado!")
        return
    
    conta = next((c for c in central_contas[cpf]["contas"] if c["numero_conta"] == numero_conta), None)
    
    if not conta:
        messagebox.showerror("Erro", "Conta não encontrada!")
        return
    
    if tipo == "Depósito":
        conta["saldo"] += valor
    elif tipo == "Saque":
        if conta["saldo"] >= valor:
            conta["saldo"] -= valor
        else:
            messagebox.showerror("Erro", "Saldo insuficiente!")
            return
    elif tipo == "Transferência":
        cpf_destino = entry_cpf_destino.get()
        numero_conta_destino = entry_numero_conta_destino.get()
        
        if cpf_destino not in central_contas:
            messagebox.showerror("Erro", "CPF de destino não encontrado!")
            return
        
        conta_destino = next((c for c in central_contas[cpf_destino]["contas"] if c["numero_conta"] == numero_conta_destino), None)
        
        if not conta_destino:
            messagebox.showerror("Erro", "Conta de destino não encontrada!")
            return
        
        if conta["saldo"] >= valor:
            conta["saldo"] -= valor
            conta_destino["saldo"] += valor
        else:
            messagebox.showerror("Erro", "Saldo insuficiente!")
            return
    
    salvar_dados(central_contas)
    messagebox.showinfo("Sucesso", f"{tipo} realizado com sucesso!")

aba_transacoes = tk.Frame(janela)

tk.Label(aba_transacoes, text="CPF do Usuário:").pack()
entry_cpf_transacao = tk.Entry(aba_transacoes)
entry_cpf_transacao.pack()

tk.Label(aba_transacoes, text="Número da Conta:").pack()
entry_numero_conta = tk.Entry(aba_transacoes)
entry_numero_conta.pack()

tk.Label(aba_transacoes, text="Valor:").pack()
entry_valor = tk.Entry(aba_transacoes)
entry_valor.pack()

tipo_transacao_var = tk.StringVar()
tipo_transacao_var.set("Depósito")  # Valor padrão

tk.Radiobutton(aba_transacoes, text="Depósito", variable=tipo_transacao_var, value="Depósito").pack()
tk.Radiobutton(aba_transacoes, text="Saque", variable=tipo_transacao_var, value="Saque").pack()
tk.Radiobutton(aba_transacoes, text="Transferência", variable=tipo_transacao_var, value="Transferência").pack()

tk.Label(aba_transacoes, text="CPF do Destinatário (apenas para transferências):").pack()
entry_cpf_destino = tk.Entry(aba_transacoes)
entry_cpf_destino.pack()

tk.Label(aba_transacoes, text="Número da Conta Destino (apenas para transferências):").pack()
entry_numero_conta_destino = tk.Entry(aba_transacoes)
entry_numero_conta_destino.pack()

btn_transacao = tk.Button(aba_transacoes, text="Realizar Transação", command=realizar_transacao)
btn_transacao.pack()

# ------- ABA DE SALDO E EXTRATO -------
def exibir_saldo_extrato():
    cpf = entry_cpf_extrato.get()
    numero_conta = entry_numero_conta_extrato.get()
    
    if cpf not in central_contas:
        messagebox.showerror("Erro", "CPF não encontrado!")
        return
    
    conta = next((c for c in central_contas[cpf]["contas"] if c["numero_conta"] == numero_conta), None)
    
    if not conta:
        messagebox.showerror("Erro", "Conta não encontrada!")
        return
    
    saldo = conta["saldo"]
    extrato = "\n".join(conta.get("extrato", ["Nenhuma transação encontrada."]))
    
    messagebox.showinfo("Saldo e Extrato", f"Saldo Atual: R$ {saldo:.2f}\n\nExtrato:\n{extrato}")

aba_extrato = tk.Frame(janela)

tk.Label(aba_extrato, text="CPF do Usuário:").pack()
entry_cpf_extrato = tk.Entry(aba_extrato)
entry_cpf_extrato.pack()

tk.Label(aba_extrato, text="Número da Conta:").pack()
entry_numero_conta_extrato = tk.Entry(aba_extrato)
entry_numero_conta_extrato.pack()

# Criando um frame para os botões de navegação (Centralizados)
frame_botoes_principais = tk.Frame(janela)
frame_botoes_principais.pack(fill="x", pady=10)

# Centralizando os botões principais dentro do frame
frame_botoes_principais.columnconfigure(0, weight=1)

btn_usuarios = tk.Button(frame_botoes_principais, text="Criar Usuário", command=lambda: mostrar_aba(aba_usuarios), width=20)
btn_usuarios.grid(row=0, column=0, padx=5, pady=5)

btn_contas = tk.Button(frame_botoes_principais, text="Criar Conta Bancária", command=lambda: mostrar_aba(aba_contas), width=20)
btn_contas.grid(row=0, column=1, padx=5, pady=5)

btn_listar = tk.Button(frame_botoes_principais, text="Listar Contas", command=lambda: mostrar_aba(aba_listar_contas), width=20)
btn_listar.grid(row=0, column=2, padx=5, pady=5)

btn_transacoes = tk.Button(frame_botoes_principais, text="Realizar Transação", command=lambda: mostrar_aba(aba_transacoes), width=20)
btn_transacoes.grid(row=1, column=0, padx=5, pady=5)

btn_extrato = tk.Button(frame_botoes_principais, text="Ver Saldo e Extrato", command=lambda: mostrar_aba(aba_extrato), width=20)
btn_extrato.grid(row=1, column=1, padx=5, pady=5)

# Criando os elementos dentro da aba de usuários
tk.Label(aba_usuarios, text="Nome:").pack(pady=2)
entry_nome = tk.Entry(aba_usuarios)
entry_nome.pack(pady=2)

tk.Label(aba_usuarios, text="Data nascimento (YYYY-MM-DD):").pack(pady=2)
entry_data_nascimento = tk.Entry(aba_usuarios)
entry_data_nascimento.pack(pady=2)

tk.Label(aba_usuarios, text="CPF:").pack(pady=2)
entry_cpf = tk.Entry(aba_usuarios)
entry_cpf.pack(pady=2)

# Criando um frame para centralizar o botão "Adicionar Usuário"
frame_btn_usuario = tk.Frame(aba_usuarios)
frame_btn_usuario.pack(pady=10)

# Botão "Adicionar Usuário" agora centralizado
btn_adicionar = tk.Button(frame_btn_usuario, text="Adicionar Usuário", command=adicionar_usuario, width=20)
btn_adicionar.pack()



# Rodar janela
janela.mainloop()