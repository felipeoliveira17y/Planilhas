import tkinter as tk
from tkinter import messagebox, ttk
import sys
from pathlib import Path

# Adiciona a raiz do projeto ao path para importar o excel corretamente
sys.path.append(str(Path(__file__).parent.parent))

from excel import ler_tabela, gerar_id_servico, adicionar_servico


class TelaServicos:

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
            text="Serviços",
            font=("Arial", 26, "bold"),
            fg="#173F2A",
            bg="#F4F7F5"
        )
        titulo.pack(side="left")

        btn_novo = tk.Button(
            topo,
            text="＋ NOVO SERVIÇO",
            command=self.abrir_formulario_novo_servico,
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
        # TABELA / LISTAGEM DE SERVIÇOS
        # ==============================
        tabela_frame = tk.Frame(self.conteudo, bg="#F4F7F5")
        tabela_frame.pack(fill="both", expand=True, padx=40, pady=(0, 40))

        colunas = ("ID", "CLIENTE", "TIPO", "STATUS", "PRIORIDADE", "VALOR")
        
        self.tree = ttk.Treeview(
            tabela_frame,
            columns=colunas,
            show="headings",
            selectmode="browse"
        )

        self.tree.heading("ID", text="ID Serviço")
        self.tree.heading("CLIENTE", text="ID Cliente")
        self.tree.heading("TIPO", text="Tipo de Serviço")
        self.tree.heading("STATUS", text="Status")
        self.tree.heading("PRIORIDADE", text="Prioridade")
        self.tree.heading("VALOR", text="Valor (R$)")

        self.tree.column("ID", width=100, anchor="w")
        self.tree.column("CLIENTE", width=100, anchor="w")
        self.tree.column("TIPO", width=220, anchor="w")
        self.tree.column("STATUS", width=130, anchor="w")
        self.tree.column("PRIORIDADE", width=110, anchor="w")
        self.tree.column("VALOR", width=110, anchor="w")

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
            servicos = ler_tabela("tbServicos")
            for s in servicos:
                valor = s.get("VALOR", "")
                valor_fmt = f"R$ {valor}" if valor else ""
                self.tree.insert(
                    "",
                    "end",
                    values=(
                        s.get("ID_SERVICO", ""),
                        s.get("ID_CLIENTE", ""),
                        s.get("TIPO_SERVICO", ""),
                        s.get("STATUS", ""),
                        s.get("PRIORIDADE", ""),
                        valor_fmt
                    )
                )
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar serviços do Excel:\n{e}")

    def abrir_formulario_novo_servico(self):
        form = tk.Toplevel(self.conteudo)
        form.title("Novo Serviço - ProAgro Consultoria")
        form.geometry("750x680")
        form.config(bg="#F4F7F5")
        form.grab_set()

        tk.Label(
            form,
            text="Cadastrar Novo Serviço",
            font=("Arial", 18, "bold"),
            fg="#173F2A",
            bg="#F4F7F5"
        ).pack(pady=(20, 10))

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

        # Buscar listas de clientes e propriedades para popular os comboboxes
        clientes_cadastrados = []
        try:
            for c in ler_tabela("tbClientes"):
                id_c = c.get("ID_CLIENTE", "")
                nome_c = c.get("NOME_RAZAO_SOCIAL", "")
                if id_c:
                    clientes_cadastrados.append(f"{id_c} - {nome_c}")
        except:
            pass

        propriedades_cadastradas = []
        try:
            for p in ler_tabela("tbPropriedades"):
                id_p = p.get("ID_PROPRIEDADE", "")
                nome_p = p.get("NOME_PROPRIEDADE", "")
                id_cli_prop = p.get("ID_CLIENTE", "")
                if id_p:
                    propriedades_cadastradas.append(f"{id_p} - {nome_p} (Cli: {id_cli_prop})")
        except:
            pass

        # ==========================================
        # CONSTRUÇÃO DOS CAMPOS (GRID DE 2 COLUNAS)
        # ==========================================
        
        # Linha 0: Cliente e Propriedade
        tk.Label(campos_frame, text="Vincular Cliente *:", font=("Arial", 9, "bold"), bg="#F4F7F5", fg="#333").grid(row=0, column=0, sticky="w", pady=(5, 0))
        tk.Label(campos_frame, text="Vincular Propriedade:", font=("Arial", 9, "bold"), bg="#F4F7F5", fg="#333").grid(row=0, column=1, sticky="w", pady=(5, 0), padx=(10, 0))

        cliente_combo = ttk.Combobox(campos_frame, values=clientes_cadastrados, state="readonly", font=("Arial", 10), width=35)
        if clientes_cadastrados:
            cliente_combo.set(clientes_cadastrados[0])
        cliente_combo.grid(row=1, column=0, sticky="ew", pady=(0, 10))

        propriedade_combo = ttk.Combobox(campos_frame, values=propriedades_cadastradas, state="readonly", font=("Arial", 10), width=35)
        if propriedades_cadastradas:
            propriedade_combo.set(propriedades_cadastradas[0])
        propriedade_combo.grid(row=1, column=1, sticky="ew", pady=(0, 10), padx=(10, 0))

        # Linha 1: Tipo de Serviço e Status
        tk.Label(campos_frame, text="Tipo de Serviço *:", font=("Arial", 9, "bold"), bg="#F4F7F5", fg="#333").grid(row=2, column=0, sticky="w", pady=(5, 0))
        tk.Label(campos_frame, text="Status:", font=("Arial", 9, "bold"), bg="#F4F7F5", fg="#333").grid(row=2, column=1, sticky="w", pady=(5, 0), padx=(10, 0))

        entry_tipo_servico = tk.Entry(campos_frame, font=("Arial", 10), relief="solid", bd=1, width=38)
        entry_tipo_servico.grid(row=3, column=0, sticky="ew", pady=(0, 10), ipady=3)

        status_combo = ttk.Combobox(campos_frame, values=["Pendente", "Em Andamento", "Concluído", "Cancelado"], state="readonly", font=("Arial", 10))
        status_combo.set("Pendente")
        status_combo.grid(row=3, column=1, sticky="ew", pady=(0, 10), padx=(10, 0))

        # Linha 2: Prioridade e Responsável
        tk.Label(campos_frame, text="Prioridade:", font=("Arial", 9, "bold"), bg="#F4F7F5", fg="#333").grid(row=4, column=0, sticky="w", pady=(5, 0))
        tk.Label(campos_frame, text="Responsável:", font=("Arial", 9, "bold"), bg="#F4F7F5", fg="#333").grid(row=4, column=1, sticky="w", pady=(5, 0), padx=(10, 0))

        prioridade_combo = ttk.Combobox(campos_frame, values=["Baixa", "Média", "Alta", "Urgente"], state="readonly", font=("Arial", 10))
        prioridade_combo.set("Média")
        prioridade_combo.grid(row=5, column=0, sticky="ew", pady=(0, 10))

        entry_responsavel = tk.Entry(campos_frame, font=("Arial", 10), relief="solid", bd=1)
        entry_responsavel.grid(row=5, column=1, sticky="ew", pady=(0, 10), padx=(10, 0), ipady=3)

        # Linha 3: Valor e Datas (Solicitação e Início)
        tk.Label(campos_frame, text="Valor (R$):", font=("Arial", 9, "bold"), bg="#F4F7F5", fg="#333").grid(row=6, column=0, sticky="w", pady=(5, 0))
        tk.Label(campos_frame, text="Data da Solicitação:", font=("Arial", 9, "bold"), bg="#F4F7F5", fg="#333").grid(row=6, column=1, sticky="w", pady=(5, 0), padx=(10, 0))

        entry_valor = tk.Entry(campos_frame, font=("Arial", 10), relief="solid", bd=1)
        entry_valor.grid(row=7, column=0, sticky="ew", pady=(0, 10), ipady=3)

        entry_data_sol = tk.Entry(campos_frame, font=("Arial", 10), relief="solid", bd=1)
        entry_data_sol.grid(row=7, column=1, sticky="ew", pady=(0, 10), padx=(10, 0), ipady=3)

        # Linha 4: Data Prevista e Data Conclusão
        tk.Label(campos_frame, text="Data Prevista:", font=("Arial", 9, "bold"), bg="#F4F7F5", fg="#333").grid(row=8, column=0, sticky="w", pady=(5, 0))
        tk.Label(campos_frame, text="Data de Conclusão:", font=("Arial", 9, "bold"), bg="#F4F7F5", fg="#333").grid(row=8, column=1, sticky="w", pady=(5, 0), padx=(10, 0))

        entry_data_prev = tk.Entry(campos_frame, font=("Arial", 10), relief="solid", bd=1)
        entry_data_prev.grid(row=9, column=0, sticky="ew", pady=(0, 10), ipady=3)

        entry_data_conc = tk.Entry(campos_frame, font=("Arial", 10), relief="solid", bd=1)
        entry_data_conc.grid(row=9, column=1, sticky="ew", pady=(0, 10), padx=(10, 0), ipady=3)

        # Linha 5: Descrição (Ocupa as duas colunas)
        tk.Label(campos_frame, text="Descrição do Serviço:", font=("Arial", 9, "bold"), bg="#F4F7F5", fg="#333").grid(row=10, column=0, columnspan=2, sticky="w", pady=(5, 0))
        entry_descricao = tk.Entry(campos_frame, font=("Arial", 10), relief="solid", bd=1)
        entry_descricao.grid(row=11, column=0, columnspan=2, sticky="ew", pady=(0, 10), ipady=3)

        # Linha 6: Observações (Ocupa as duas colunas)
        tk.Label(campos_frame, text="Observações:", font=("Arial", 9, "bold"), bg="#F4F7F5", fg="#333").grid(row=12, column=0, columnspan=2, sticky="w", pady=(5, 0))
        entry_obs = tk.Entry(campos_frame, font=("Arial", 10), relief="solid", bd=1)
        entry_obs.grid(row=13, column=0, columnspan=2, sticky="ew", pady=(0, 15), ipady=3)

        # ==========================================
        # BOTÃO SALVAR
        # ==========================================
        def salvar():
            tipo_serv = entry_tipo_servico.get().strip()
            if not tipo_serv:
                messagebox.showwarning("Aviso", "O campo Tipo de Serviço é obrigatório!", parent=form)
                return

            cliente_selecionado = cliente_combo.get()
            if not cliente_selecionado:
                messagebox.showwarning("Aviso", "Você precisa selecionar um cliente!", parent=form)
                return

            id_cliente = cliente_selecionado.split(" - ")[0]
            
            id_propriedade = ""
            prop_selecionada = propriedade_combo.get()
            if prop_selecionada:
                id_propriedade = prop_selecionada.split(" - ")[0]

            try:
                novo_id_servico = gerar_id_servico()

                dados = {
                    "ID_SERVICO": novo_id_servico,
                    "ID_CLIENTE": id_cliente,
                    "ID_PROPRIEDADE": id_propriedade,
                    "TIPO_SERVICO": tipo_serv,
                    "DESCRICAO": entry_descricao.get().strip(),
                    "STATUS": status_combo.get(),
                    "PRIORIDADE": prioridade_combo.get(),
                    "DATA_SOLICITACAO": entry_data_sol.get().strip(),
                    "DATA_INICIO": "",
                    "DATA_PREVISTA": entry_data_prev.get().strip(),
                    "DATA_CONCLUSAO": entry_data_conc.get().strip(),
                    "RESPONSAVEL": entry_responsavel.get().strip(),
                    "VALOR": entry_valor.get().strip(),
                    "OBSERVACOES": entry_obs.get().strip(),
                    "DATA_CADASTRO": ""
                }

                adicionar_servico(dados)

                messagebox.showinfo("Sucesso", f"Serviço {novo_id_servico} cadastrado com sucesso!", parent=form)
                form.destroy()
                self.carregar_dados()

            except Exception as e:
                messagebox.showerror("Erro", f"Ocorreu um erro ao salvar o serviço:\n{e}", parent=form)

        btn_salvar = tk.Button(
            campos_frame,
            text="Salvar Serviço",
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
        btn_salvar.grid(row=14, column=0, columnspan=2, sticky="ew", pady=(10, 20))