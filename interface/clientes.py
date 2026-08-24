import tkinter as tk
from tkinter import messagebox, ttk
import sys
from pathlib import Path

# Adiciona a raiz do projeto ao path para importar o excel e pastas corretamente
sys.path.append(str(Path(__file__).parent.parent))

from excel import ler_tabela, gerar_id_cliente, adicionar_cliente
from pastas import criar_pasta_cliente


class TelaClientes:

    def __init__(self, conteudo_frame, dashboard_ref):
        self.conteudo = conteudo_frame
        self.dashboard = dashboard_ref
        self.renderizar()

    def limpar_conteudo(self):
        for widget in self.conteudo.winfo_children():
            widget.destroy()

    def renderizar(self):
        self.limpar_conteudo()

        # ==============================
        # TOPO DA TELA
        # ==============================
        topo = tk.Frame(self.conteudo, bg="#F4F7F5")
        topo.pack(fill="x", padx=40, pady=(35, 20))

        titulo = tk.Label(
            topo,
            text="Clientes",
            font=("Arial", 26, "bold"),
            fg="#173F2A",
            bg="#F4F7F5"
        )
        titulo.pack(side="left")

        btn_novo = tk.Button(
            topo,
            text="＋ NOVO CLIENTE",
            command=self.abrir_formulario_novo_cliente,
            font=("Arial", 10, "bold"),
            fg="white",
            bg="#245C3E",
            activebackground="#173F2A",
            activeforeground="white",
            relief="flat",
            padx=15,
            pady=10,
            cursor="hand2"
        )
        btn_novo.pack(side="right")

        # ==============================
        # TABELA / LISTAGEM DE CLIENTES
        # ==============================
        tabela_frame = tk.Frame(self.conteudo, bg="#F4F7F5")
        tabela_frame.pack(fill="both", expand=True, padx=40, pady=(0, 40))

        # Configuração do Treeview (Tabela estilizada)
        colunas = ("ID", "NOME", "TIPO", "TELEFONE", "CIDADE")
        
        self.tree = ttk.Treeview(
            tabela_frame,
            columns=colunas,
            show="headings",
            selectmode="browse"
        )

        # Definindo cabeçalhos
        self.tree.heading("ID", text="ID")
        self.tree.heading("NOME", text="Nome / Razão Social")
        self.tree.heading("TIPO", text="Tipo")
        self.tree.heading("TELEFONE", text="Telefone")
        self.tree.heading("CIDADE", text="Cidade")

        # Definindo largura das colunas
        self.tree.column("ID", width=100, anchor="w")
        self.tree.column("NOME", width=300, anchor="w")
        self.tree.column("TIPO", width=150, anchor="w")
        self.tree.column("TELEFONE", width=150, anchor="w")
        self.tree.column("CIDADE", width=150, anchor="w")

        # Scrollbar para a tabela
        scrollbar = ttk.Scrollbar(
            tabela_frame,
            orient="vertical",
            command=self.tree.yview
        )
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Carregar os dados do Excel na tabela
        self.carregar_dados()

    def carregar_dados(self):
        # Limpa itens atuais da tela
        for item in self.tree.get_children():
            self.tree.delete(item)

        try:
            clientes = ler_tabela("tbClientes")
            for c in clientes:
                self.tree.insert(
                    "",
                    "end",
                    values=(
                        c.get("ID_CLIENTE", ""),
                        c.get("NOME_RAZAO_SOCIAL", ""),
                        c.get("TIPO_CLIENTE", ""),
                        c.get("TELEFONE", ""),
                        c.get("CIDADE", "")
                    )
                )
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar clientes do Excel:\n{e}")

    def abrir_formulario_novo_cliente(self):
        # Janela Toplevel para o Formulário
        form = tk.Toplevel(self.conteudo)
        form.title("Novo Cliente - ProAgro Consultoria")
        form.geometry("500x600")
        form.config(bg="#F4F7F5")
        form.grab_set()  # Torna a janela modal

        tk.Label(
            form,
            text="Cadastrar Novo Cliente",
            font=("Arial", 16, "bold"),
            fg="#173F2A",
            bg="#F4F7F5"
        ).pack(pady=(20, 15))

        # Campos do Formulário
        campos_frame = tk.Frame(form, bg="#F4F7F5")
        campos_frame.pack(fill="both", expand=True, padx=30)

        tk.Label(campos_frame, text="Tipo de Cliente:", font=("Arial", 10, "bold"), bg="#F4F7F5", fg="#333").pack(anchor="w", pady=(5, 0))
        tipo_combo = ttk.Combobox(campos_frame, values=["Pessoa Física", "Pessoa Jurídica"], state="readonly", font=("Arial", 10))
        tipo_combo.set("Pessoa Física")
        tipo_combo.pack(fill="x", pady=(0, 10))

        tk.Label(campos_frame, text="Nome / Razão Social:", font=("Arial", 10, "bold"), bg="#F4F7F5", fg="#333").pack(anchor="w", pady=(5, 0))
        entry_nome = tk.Entry(campos_frame, font=("Arial", 10), relief="solid", bd=1)
        entry_nome.pack(fill="x", pady=(0, 10), ipady=4)

        tk.Label(campos_frame, text="Telefone:", font=("Arial", 10, "bold"), bg="#F4F7F5", fg="#333").pack(anchor="w", pady=(5, 0))
        entry_tel = tk.Entry(campos_frame, font=("Arial", 10), relief="solid", bd=1)
        entry_tel.pack(fill="x", pady=(0, 10), ipady=4)

        tk.Label(campos_frame, text="Cidade:", font=("Arial", 10, "bold"), bg="#F4F7F5", fg="#333").pack(anchor="w", pady=(5, 0))
        entry_cidade = tk.Entry(campos_frame, font=("Arial", 10), relief="solid", bd=1)
        entry_cidade.pack(fill="x", pady=(0, 10), ipady=4)

        tk.Label(campos_frame, text="Observações:", font=("Arial", 10, "bold"), bg="#F4F7F5", fg="#333").pack(anchor="w", pady=(5, 0))
        entry_obs = tk.Entry(campos_frame, font=("Arial", 10), relief="solid", bd=1)
        entry_obs.pack(fill="x", pady=(0, 20), ipady=4)

        def salvar():
            nome = entry_nome.get().strip()
            if not nome:
                messagebox.showwarning("Aviso", "O campo Nome / Razão Social é obrigatório!", parent=form)
                return

            try:
                # 1. Gera ID automático
                novo_id = gerar_id_cliente()

                # 2. Monta o dicionário de dados estruturado para a tbClientes
                dados = {
                    "ID_CLIENTE": novo_id,
                    "TIPO_CLIENTE": tipo_combo.get(),
                    "ID_TIPO_CLIENTE": "",
                    "NOME_RAZAO_SOCIAL": nome,
                    "CPF_CNPJ": "",
                    "RG_IE": "",
                    "TELEFONE": entry_tel.get().strip(),
                    "EMAIL": "",
                    "CEP": "",
                    "ENDERECO": "",
                    "NUMERO": "",
                    "COMPLEMENTO": "",
                    "BAIRRO": "",
                    "CIDADE": entry_cidade.get().strip(),
                    "UF": "",
                    "OBSERVACOES": entry_obs.get().strip(),
                    "DATA_CADASTRO": "",
                    "ATIVO": "SIM"
                }

                # 3. Salva no Excel
                adicionar_cliente(dados)

                # 4. Cria a estrutura de pastas automaticamente
                criar_pasta_cliente(novo_id, nome)

                messagebox.cesso = messagebox.showinfo("Sucesso", f"Cliente {novo_id} cadastrado e pastas criadas com sucesso!", parent=form)
                
                form.destroy()
                self.carregar_dados() # Atualiza a tabela na tela principal

            except Exception as e:
                messagebox.showerror("Erro", f"Ocorreu um erro ao salvar o cliente:\n{e}", parent=form)

        btn_salvar = tk.Button(
            campos_frame,
            text="Salvar Cliente",
            command=salvar,
            font=("Arial", 11, "bold"),
            fg="white",
            bg="#173F2A",
            activebackground="#245C3E",
            activeforeground="white",
            relief="flat",
            pady=10,
            cursor="hand2"
        )
        btn_salvar.pack(fill="x", pady=10)