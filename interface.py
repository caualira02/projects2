#!/usr/bin/env python3
"""
Sistema Bancário
----------------
Este sistema permite o cadastro de usuários, criação de contas, depósito e saque,
persistindo os dados em um arquivo JSON. Todas as mensagens e variáveis estão em português.
"""

import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime
from usuarios import criar_usuario  # Função para criar o usuário
from endereco import criar_endereco  # Função para criar o endereço
from database import salvar_dados, carregar_dados  # Funções de salvar e carregar dados
import os

class SistemaBancario:
    def __init__(self, master):
        self.master = master
        self.master.title("Sistema Bancário")
        self.central_contas = carregar_dados()  # Carrega os dados do arquivo JSON
        
        # Cria as abas usando Notebook
        self.notebook = ttk.Notebook(self.master)
        self.notebook.pack(expand=1, fill="both")
        
        # Criação das abas
        self.criar_aba_cadastro()
        self.criar_aba_deposito()
        self.criar_aba_saque()
    
    # --- Métodos de lógica do sistema ---
    
    def cadastrar_usuario(self):
        """
        Método chamado quando o usuário clica no botão de cadastro.
        Lê os campos, valida os dados, chama a função de criar usuário (do módulo usuarios)
        e atualiza os dados persistidos.
        """
        try:
            cpf = self.entry_cpf.get().strip()
            nome = self.entry_nome.get().strip()
            data_nascimento = self.entry_data_nascimento.get().strip()
            cep = self.entry_cep.get().strip()
            bairro = self.entry_bairro.get().strip()
            cidade = self.entry_cidade.get().strip()
            estado = self.entry_estado.get().strip()
            logradouro = self.entry_logradouro.get().strip()
            numero_casa = self.entry_numero_casa.get().strip()
            
            # Verifica campos obrigatórios
            if not cpf or not nome or not data_nascimento:
                raise ValueError("Preencha todos os campos obrigatórios.")
            
            # Verifica se o CPF já existe
            if cpf in self.central_contas:
                raise ValueError(f"O CPF {cpf} já está cadastrado.")
            
            # Chama a função para criar o usuário (do módulo usuarios)
            # Observe que a função 'criar_usuario' já usa 'criar_endereco' internamente,
            # conforme seu módulo.
            usuario = criar_usuario(self.central_contas, cpf, nome, data_nascimento, cep, bairro, cidade, estado, logradouro, numero_casa)
            
            if usuario:
                messagebox.showinfo("Sucesso", f"Usuário {nome} criado com sucesso!")
                salvar_dados(self.central_contas)
                self.central_contas = carregar_dados()  # Atualiza os dados
                self.limpar_campos_cadastro()
            else:
                raise Exception("Erro ao criar o usuário.")
        except ValueError as ve:
            messagebox.showerror("Erro", str(ve))
        except Exception as e:
            messagebox.showerror("Erro", str(e))
    
    def efetuar_deposito(self):
        """
        Método para realizar depósito.
        Lê os campos da aba de depósito, valida os dados e atualiza o saldo e extrato.
        """
        try:
            cpf = self.entry_cpf_deposito.get().strip()
            num_conta = self.entry_numero_conta_deposito.get().strip()
            valor_deposito = float(self.entry_valor_deposito.get().strip())
            
            if cpf not in self.central_contas:
                raise ValueError("CPF não encontrado.")
            
            conta = None
            for c in self.central_contas[cpf]["contas"]:
                if c["numero_conta"] == int(num_conta):
                    conta = c
                    break
            
            if not conta:
                raise ValueError("Número da conta não encontrado.")
            
            if valor_deposito <= 0:
                raise ValueError("Valor de depósito inválido.")
            
            conta["saldo"] += valor_deposito
            conta["extrato"].append({
                "data_hora": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "valor": valor_deposito
            })
            
            messagebox.showinfo("Sucesso", f"Depósito de R$ {valor_deposito:.2f} realizado com sucesso!")
            salvar_dados(self.central_contas)
            self.central_contas = carregar_dados()
            self.limpar_campos_deposito()
        except ValueError as ve:
            messagebox.showerror("Erro", str(ve))
        except Exception as e:
            messagebox.showerror("Erro", str(e))
    
    def efetuar_saque(self):
        """
        Método para realizar saque.
        Lê os campos da aba de saque, valida os dados, verifica o saldo e atualiza o extrato.
        """
        try:
            cpf = self.entry_cpf_saque.get().strip()
            num_conta = self.entry_numero_conta_saque.get().strip()
            valor_saque = float(self.entry_valor_saque.get().strip())
            
            if cpf not in self.central_contas:
                raise ValueError("CPF não encontrado.")
            
            conta = None
            for c in self.central_contas[cpf]["contas"]:
                if c["numero_conta"] == int(num_conta):
                    conta = c
                    break
            
            if not conta:
                raise ValueError("Número da conta não encontrado.")
            
            if valor_saque <= 0:
                raise ValueError("Valor de saque inválido.")
            if valor_saque > conta["saldo"]:
                raise ValueError("Saldo insuficiente para saque.")
            
            conta["saldo"] -= valor_saque
            conta["extrato"].append({
                "data_hora": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "valor": -valor_saque
            })
            
            messagebox.showinfo("Sucesso", f"Saque de R$ {valor_saque:.2f} realizado com sucesso!")
            salvar_dados(self.central_contas)
            self.central_contas = carregar_dados()
            self.limpar_campos_saque()
        except ValueError as ve:
            messagebox.showerror("Erro", str(ve))
        except Exception as e:
            messagebox.showerror("Erro", str(e))
    
    # --- Métodos para limpar campos ---
    
    def limpar_campos_cadastro(self):
        self.entry_cpf.delete(0, tk.END)
        self.entry_nome.delete(0, tk.END)
        self.entry_data_nascimento.delete(0, tk.END)
        self.entry_cep.delete(0, tk.END)
        self.entry_bairro.delete(0, tk.END)
        self.entry_cidade.delete(0, tk.END)
        self.entry_estado.delete(0, tk.END)
        self.entry_logradouro.delete(0, tk.END)
        self.entry_numero_casa.delete(0, tk.END)
    
    def limpar_campos_deposito(self):
        self.entry_cpf_deposito.delete(0, tk.END)
        self.entry_numero_conta_deposito.delete(0, tk.END)
        self.entry_valor_deposito.delete(0, tk.END)
    
    def limpar_campos_saque(self):
        self.entry_cpf_saque.delete(0, tk.END)
        self.entry_numero_conta_saque.delete(0, tk.END)
        self.entry_valor_saque.delete(0, tk.END)
    
    # --- Métodos para construir as abas da interface ---
    
    def criar_aba_cadastro(self):
        """Cria a aba de cadastro de usuário."""
        aba = ttk.Frame(self.notebook)
        self.notebook.add(aba, text="Cadastro de Usuário")
        
        # CPF
        lbl_cpf = tk.Label(aba, text="CPF:")
        lbl_cpf.grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.entry_cpf = tk.Entry(aba)
        self.entry_cpf.grid(row=0, column=1, padx=5, pady=5)
        
        # Nome
        lbl_nome = tk.Label(aba, text="Nome:")
        lbl_nome.grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.entry_nome = tk.Entry(aba)
        self.entry_nome.grid(row=1, column=1, padx=5, pady=5)
        
        # Data de Nascimento
        lbl_data = tk.Label(aba, text="Data de Nascimento (AAAA-MM-DD):")
        lbl_data.grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.entry_data_nascimento = tk.Entry(aba)
        self.entry_data_nascimento.grid(row=2, column=1, padx=5, pady=5)
        
        # CEP
        lbl_cep = tk.Label(aba, text="CEP:")
        lbl_cep.grid(row=3, column=0, padx=5, pady=5, sticky="e")
        self.entry_cep = tk.Entry(aba)
        self.entry_cep.grid(row=3, column=1, padx=5, pady=5)
        
        # Bairro
        lbl_bairro = tk.Label(aba, text="Bairro:")
        lbl_bairro.grid(row=4, column=0, padx=5, pady=5, sticky="e")
        self.entry_bairro = tk.Entry(aba)
        self.entry_bairro.grid(row=4, column=1, padx=5, pady=5)
        
        # Cidade
        lbl_cidade = tk.Label(aba, text="Cidade:")
        lbl_cidade.grid(row=5, column=0, padx=5, pady=5, sticky="e")
        self.entry_cidade = tk.Entry(aba)
        self.entry_cidade.grid(row=5, column=1, padx=5, pady=5)
        
        # Estado
        lbl_estado = tk.Label(aba, text="Estado:")
        lbl_estado.grid(row=6, column=0, padx=5, pady=5, sticky="e")
        self.entry_estado = tk.Entry(aba)
        self.entry_estado.grid(row=6, column=1, padx=5, pady=5)
        
        # Logradouro
        lbl_logradouro = tk.Label(aba, text="Logradouro:")
        lbl_logradouro.grid(row=7, column=0, padx=5, pady=5, sticky="e")
        self.entry_logradouro = tk.Entry(aba)
        self.entry_logradouro.grid(row=7, column=1, padx=5, pady=5)
        
        # Número da Casa
        lbl_numero = tk.Label(aba, text="Número da Casa:")
        lbl_numero.grid(row=8, column=0, padx=5, pady=5, sticky="e")
        self.entry_numero_casa = tk.Entry(aba)
        self.entry_numero_casa.grid(row=8, column=1, padx=5, pady=5)
        
        # Botão de cadastro
        btn_cadastrar = tk.Button(aba, text="Adicionar Usuário", command=self.cadastrar_usuario)
        btn_cadastrar.grid(row=9, column=0, columnspan=2, pady=10)
    
    def criar_aba_deposito(self):
        """Cria a aba de depósito."""
        aba = ttk.Frame(self.notebook)
        self.notebook.add(aba, text="Depósito")
        
        # CPF para depósito
        lbl_cpf_dep = tk.Label(aba, text="CPF:")
        lbl_cpf_dep.grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.entry_cpf_deposito = tk.Entry(aba)
        self.entry_cpf_deposito.grid(row=0, column=1, padx=5, pady=5)
        
        # Número da Conta para depósito
        lbl_num_conta_dep = tk.Label(aba, text="Número da Conta:")
        lbl_num_conta_dep.grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.entry_numero_conta_deposito = tk.Entry(aba)
        self.entry_numero_conta_deposito.grid(row=1, column=1, padx=5, pady=5)
        
        # Valor do Depósito
        lbl_valor_dep = tk.Label(aba, text="Valor do Depósito:")
        lbl_valor_dep.grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.entry_valor_deposito = tk.Entry(aba)
        self.entry_valor_deposito.grid(row=2, column=1, padx=5, pady=5)
        
        # Botão de depósito
        btn_depositar = tk.Button(aba, text="Depositar", command=self.efetuar_deposito)
        btn_depositar.grid(row=3, column=0, columnspan=2, pady=10)
    
    def criar_aba_saque(self):
        """Cria a aba de saque."""
        aba = ttk.Frame(self.notebook)
        self.notebook.add(aba, text="Saque")
        
        # CPF para saque
        lbl_cpf_saq = tk.Label(aba, text="CPF:")
        lbl_cpf_saq.grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.entry_cpf_saque = tk.Entry(aba)
        self.entry_cpf_saque.grid(row=0, column=1, padx=5, pady=5)
        
        # Número da Conta para saque
        lbl_num_conta_saq = tk.Label(aba, text="Número da Conta:")
        lbl_num_conta_saq.grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.entry_numero_conta_saque = tk.Entry(aba)
        self.entry_numero_conta_saque.grid(row=1, column=1, padx=5, pady=5)
        
        # Valor do Saque
        lbl_valor_saq = tk.Label(aba, text="Valor do Saque:")
        lbl_valor_saq.grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.entry_valor_saque = tk.Entry(aba)
        self.entry_valor_saque.grid(row=2, column=1, padx=5, pady=5)
        
        # Botão de saque
        btn_sacar = tk.Button(aba, text="Sacar", command=self.efetuar_saque)
        btn_sacar.grid(row=3, column=0, columnspan=2, pady=10)


if __name__ == "__main__":
    root = tk.Tk()
    app = SistemaBancario(root)
    root.mainloop()
