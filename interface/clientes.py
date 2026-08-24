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

        colunas = ("ID", "NOME", "TIPO", "TELEFONE", "CIDADE")
        
        self.tree = ttk.Treeview(
            tabela_frame,
            columns=colunas,
            show="headings",
            selectmode="browse"
        )

        self.tree.heading("ID", text="ID")
        self.tree.heading("NOME", text="Nome / Razão Social")
        self.tree.heading("TIPO", text="Tipo")
        self.tree.heading("TELEFONE", text="Telefone")
        self.tree.heading("CIDADE", text="Cidade")

        self.tree.column("ID", width=100, anchor="w")
        self.tree.column("NOME", width=300, anchor="w")
        self.tree.column("TIPO", width=150, anchor="w")
        self.tree.column("TELEFONE", width=150, anchor="w")
        self.tree.column("CIDADE", width=150, anchor="w")

        scrollbar = ttk.Scrollbar(
            tabela_frame,
            orient="vertical",
            command=self.tree.yview
        )
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.carregar_dados()

    def carregar_dados(self):
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
        # Janela Toplevel maior para acomodar todos os campos com rolagem
        form = tk.Toplevel(self.conteudo)
        form.title("Novo Cliente - ProAgro Consultoria")
        form.geometry("750x650")
        form.config(bg="#F4F7F5")
        form.grab_set()

        # Título do Formulário
        tk.Label(
            form,
            text="Cadastrar Novo Cliente",
            font=("Arial", 18, "bold"),
            fg="#173F2A",
            bg="#F4F7F5"
        ).pack(pady=(20, 10))

        # Canvas e Scrollbar para o formulário longo
        container = tk.Frame(form, bg="#F4F7F5")
        container.pack(fill="both", expand=True, padx=20, pady=10)

        canvas = tk.Canvas(container, bg="#F4F7F5", highlightthickness=0)
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
        
        campos_frame = tk.Frame(canvas, bg="#F4F7F5")
        campos_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=campos_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # ==========================================
        # FUNÇÕES DE MÁSCARA (FORMATAÇÃO AUTOMÁTICA)
        # ==========================================
        def formatar_telefone(event):
            texto = entry_tel.get()
            # Remove tudo que não é dígito
            digitos = "".join(filter(str.isdigit, texto))[:11]
            formatado = ""
            if len(digitos) > 10:  # Celular com 9º dígito: (XX) 9XXXX-XXXX
                formatado = f"({digitos[:2]}) {digitos[2]} {digitos[3:7]}-{digitos[7:]}" if len(digitos) > 7 else f"({digitos[:2]}) {digitos[2:]}"
            elif len(digitos) > 6:  # (XX) XXXX-XXXX
                formatado = f"({digitos[:2]}) {digitos[2:6]}-{digitos[6:]}"
            elif len(digitos) > 2:
                formatado = f"({digitos[:2]}) {digitos[2:]}"
            elif len(digitos) > 0:
                formatado = f"({digitos}"
            
            entry_tel.delete(0, tk.END)
            entry_tel.insert(0, formatado)

        def formatar_cpf_cnpj(event):
            texto = entry_cpf_cnpj.get()
            digitos = "".join(filter(str.isdigit, texto))[:14] # Máximo CNPJ (14 dígitos)
            formatado = ""
            
            if len(digitos) <= 11:  # CPF: 000.000.000-00
                if len(digitos) > 9:
                    formatado = f"{digitos[:3]}.{digitos[3:6]}:{digitos[6:9]}-{digitos[9:]}" # Ajuste fino abaixo
                    formatado = f"{digitos[:3]}.{digitos[3:6]}.{digitos[6:9]}-{digitos[9:]}"
                elif len(digitos) > 6:
                    formatado = f"{digitos[:3]}.{digitos[3:6]}.{digitos[6:]}"
                elif len(digitos) > 3:
                    formatado = f"{digitos[:3]}.{digitos[3:]}"
                else:
                    formatado = digitos
            else:  # CNPJ: 00.000.000/0000-00
                formatado = f"{digitos[:2]}.{digitos[2:5]}.{digitos[5:8]}/{digitos[8:12]}-{digitos[12:]}"

            entry_cpf_cnpj.delete(0, tk.END)
            entry_cpf_cnpj.insert(0, formatado)

        # ==========================================
        # CONSTRUÇÃO DOS CAMPOS (GRID DE 2 COLUNAS)
        # ==========================================
        
        # Linha 0: Tipo e Nome
        tk.Label(campos_frame, text="Tipo de Cliente:", font=("Arial", 9, "bold"), bg="#F4F7F5", fg="#333").grid(row=0, column=0, sticky="w", pady=(5, 0))
        tk.Label(campos_frame, text="Nome / Razão Social *:", font=("Arial", 9, "bold"), bg="#F4F7F5", fg="#333").grid(row=0, column=1, sticky="w", pady=(5, 0), padx=(10, 0))

        tipo_combo = ttk.Combobox(campos_frame, values=["Pessoa Física", "Pessoa Jurídica"], state="readonly", font=("Arial", 10), width=22)
        tipo_combo.set("Pessoa Física")
        tipo_combo.grid(row=1, column=0, sticky="ew", pady=(0, 10))

        entry_nome = tk.Entry(campos_frame, font=("Arial", 10), relief="solid", bd=1, width=38)
        entry_nome.grid(row=1, column=1, sticky="ew", pady=(0, 10), padx=(10, 0), ipady=3)

        # Linha 1: CPF/CNPJ e RG/IE
        tk.Label(campos_frame, text="CPF / CNPJ:", font=("Arial", 9, "bold"), bg="#F4F7F5", fg="#333").grid(row=2, column=0, sticky="w", pady=(5, 0))
        tk.Label(campos_frame, text="RG / IE:", font=("Arial", 9, "bold"), bg="#F4F7F5", fg="#333").grid(row=2, column=1, sticky="w", pady=(5, 0), padx=(10, 0))

        entry_cpf_cnpj = tk.Entry(campos_frame, font=("Arial", 10), relief="solid", bd=1)
        entry_cpf_cnpj.grid(row=3, column=0, sticky="ew", pady=(0, 10), ipady=3)
        entry_cpf_cnpj.bind("<KeyRelease>", formatar_cpf_cnpj)

        entry_rg_ie = tk.Entry(campos_frame, font=("Arial", 10), relief="solid", bd=1)
        entry_rg_ie.grid(row=3, column=1, sticky="ew", pady=(0, 10), padx=(10, 0), ipady=3)

        # Linha 2: Telefone e E-mail
        tk.Label(campos_frame, text="Telefone:", font=("Arial", 9, "bold"), bg="#F4F7F5", fg="#333").grid(row=4, column=0, sticky="w", pady=(5, 0))
        tk.Label(campos_frame, text="E-mail:", font=("Arial", 9, "bold"), bg="#F4F7F5", fg="#333").grid(row=4, column=1, sticky="w", pady=(5, 0), padx=(10, 0))

        entry_tel = tk.Entry(campos_frame, font=("Arial", 10), relief="solid", bd=1)
        entry_tel.grid(row=5, column=0, sticky="ew", pady=(0, 10), ipady=3)
        entry_tel.bind("<KeyRelease>", formatar_telefone)

        entry_email = tk.Entry(campos_frame, font=("Arial", 10), relief="solid", bd=1)
        entry_email.grid(row=5, column=1, sticky="ew", pady=(0, 10), padx=(10, 0), ipady=3)

        # Linha 3: CEP e Endereço
        tk.Label(campos_frame, text="CEP:", font=("Arial", 9, "bold"), bg="#F4F7F5", fg="#333").grid(row=6, column=0, sticky="w", pady=(5, 0))
        tk.Label(campos_frame, text="Endereço (Logradouro):", font=("Arial", 9, "bold"), bg="#F4F7F5", fg="#333").grid(row=6, column=1, sticky="w", pady=(5, 0), padx=(10, 0))

        entry_cep = tk.Entry(campos_frame, font=("Arial", 10), relief="solid", bd=1)
        entry_cep.grid(row=7, column=0, sticky="ew", pady=(0, 10), ipady=3)

        entry_endereco = tk.Entry(campos_frame, font=("Arial", 10), relief="solid", bd=1)
        entry_endereco.grid(row=7, column=1, sticky="ew", pady=(0, 10), padx=(10, 0), ipady=3)

        # Linha 4: Número e Complemento
        tk.Label(campos_frame, text="Número:", font=("Arial", 9, "bold"), bg="#F4F7F5", fg="#333").grid(row=8, column=0, sticky="w", pady=(5, 0))
        tk.Label(campos_frame, text="Complemento:", font=("Arial", 9, "bold"), bg="#F4F7F5", fg="#333").grid(row=8, column=1, sticky="w", pady=(5, 0), padx=(10, 0))

        entry_numero = tk.Entry(campos_frame, font=("Arial", 10), relief="solid", bd=1)
        entry_numero.grid(row=9, column=0, sticky="ew", pady=(0, 10), ipady=3)

        entry_complemento = tk.Entry(campos_frame, font=("Arial", 10), relief="solid", bd=1)
        entry_complemento.grid(row=9, column=1, sticky="ew", pady=(0, 10), padx=(10, 0), ipady=3)

        # Linha 5: Bairro e Cidade
        tk.Label(campos_frame, text="Bairro:", font=("Arial", 9, "bold"), bg="#F4F7F5", fg="#333").grid(row=10, column=0, sticky="w", pady=(5, 0))
        tk.Label(campos_frame, text="Cidade:", font=("Arial", 9, "bold"), bg="#F4F7F5", fg="#333").grid(row=10, column=1, sticky="w", pady=(5, 0), padx=(10, 0))

        entry_bairro = tk.Entry(campos_frame, font=("Arial", 10), relief="solid", bd=1)
        entry_bairro.grid(row=11, column=0, sticky="ew", pady=(0, 10), ipady=3)

        entry_cidade = tk.Entry(campos_frame, font=("Arial", 10), relief="solid", bd=1)
        entry_cidade.grid(row=11, column=1, sticky="ew", pady=(0, 10), padx=(10, 0), ipady=3)

        # Linha 6: UF
        tk.Label(campos_frame, text="UF (Estado):", font=("Arial", 9, "bold"), bg="#F4F7F5", fg="#333").grid(row=12, column=0, sticky="w", pady=(5, 0))
        entry_uf = tk.Entry(campos_frame, font=("Arial", 10), relief="solid", bd=1)
        entry_uf.grid(row=13, column=0, sticky="ew", pady=(0, 10), ipady=3)

        # Linha 7: Observações (Ocupa as duas colunas)
        tk.Label(campos_frame, text="Observações:", font=("Arial", 9, "bold"), bg="#F4F7F5", fg="#333").grid(row=14, column=0, columnspan=2, sticky="w", pady=(5, 0))
        entry_obs = tk.Entry(campos_frame, font=("Arial", 10), relief="solid", bd=1)
        entry_obs.grid(row=15, column=0, columnspan=2, sticky="ew", pady=(0, 15), ipady=3)

        # ==========================================
        # BOTÃO SALVAR
        # ==========================================
        def salvar():
            nome = entry_nome.get().strip()
            if not nome:
                messagebox.showwarning("Aviso", "O campo Nome / Razão Social é obrigatório!", parent=form)
                return

            try:
                # 1. Gera ID automático
                novo_id = gerar_id_cliente()

                # 2. Monta o dicionário completo mapeado exatamente com a tbClientes
                dados = {
                    "ID_CLIENTE": novo_id,
                    "TIPO_CLIENTE": tipo_combo.get(),
                    "ID_TIPO_CLIENTE": "",
                    "NOME_RAZAO_SOCIAL": nome,
                    "CPF_CNPJ": entry_cpf_cnpj.get().strip(),
                    "RG_IE": entry_rg_ie.get().strip(),
                    "TELEFONE": entry_tel.get().strip(),
                    "EMAIL": entry_email.get().strip(),
                    "CEP": entry_cep.get().strip(),
                    "ENDERECO": entry_endereco.get().strip(),
                    "NUMERO": entry_numero.get().strip(),
                    "COMPLEMENTO": entry_complemento.get().strip(),
                    "BAIRRO": entry_bairro.get().strip(),
                    "CIDADE": entry_cidade.get().strip(),
                    "UF": entry_uf.get().strip().upper(),
                    "OBSERVACOES": entry_obs.get().strip(),
                    "DATA_CADASTRO": "",
                    "ATIVO": "SIM"
                }

                # 3. Salva no Excel
                adicionar_cliente(dados)

                # 4. Cria as pastas automáticas no Windows
                criar_pasta_cliente(novo_id, nome)

                messagebox.showinfo("Sucesso", f"Cliente {novo_id} cadastrado, gravado no Excel e pastas criadas com sucesso!", parent=form)
                
                form.destroy()
                self.carregar_dados()

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
        btn_salvar.grid(row=16, column=0, columnspan=2, sticky="ew", pady=(10, 20))