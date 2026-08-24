import tkinter as tk
from tkinter import messagebox, ttk
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))
from excel import ler_tabela, gerar_id_equipamento, adicionar_equipamento


class TelaEquipamentos:

    def __init__(self, conteudo_frame, dashboard_ref):
        self.conteudo = conteudo_frame
        self.dashboard = dashboard_ref
        self.renderizar()

    def limpar_conteudo(self):
        for widget in self.conteudo.winfo_children():
            widget.destroy()

    def renderizar(self):
        self.limpar_conteudo()

        topo = tk.Frame(self.conteudo, bg="#F4F7F5")
        topo.pack(fill="x", padx=40, pady=(35, 20))

        titulo = tk.Label(topo, text="Equipamentos", font=("Arial", 26, "bold"), fg="#173F2A", bg="#F4F7F5")
        titulo.pack(side="left")

        btn_novo = tk.Button(
            topo, text="＋ NOVO EQUIPAMENTO", command=self.abrir_formulario,
            font=("Arial", 10, "bold"), fg="white", bg="#245C3E", relief="flat", padx=15, pady=10, cursor="hand2"
        )
        btn_novo.pack(side="right")

        tabela_frame = tk.Frame(self.conteudo, bg="#F4F7F5")
        tabela_frame.pack(fill="both", expand=True, padx=40, pady=(0, 40))

        colunas = ("ID", "TIPO", "NOME", "MARCA", "STATUS", "CONSERVACAO")
        self.tree = ttk.Treeview(tabela_frame, columns=colunas, show="headings", selectmode="browse")

        self.tree.heading("ID", text="ID")
        self.tree.heading("TIPO", text="Tipo")
        self.tree.heading("NOME", text="Nome")
        self.tree.heading("MARCA", text="Marca")
        self.tree.heading("STATUS", text="Status")
        self.tree.heading("CONSERVACAO", text="Conservação")

        self.tree.column("ID", width=100, anchor="w")
        self.tree.column("TIPO", width=140, anchor="w")
        self.tree.column("NOME", width=200, anchor="w")
        self.tree.column("MARCA", width=130, anchor="w")
        self.tree.column("STATUS", width=110, anchor="w")
        self.tree.column("CONSERVACAO", width=130, anchor="w")

        scrollbar = ttk.Scrollbar(tabela_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.carregar_dados()

    def carregar_dados(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        try:
            for eq in ler_tabela("tbEquipamentos"):
                self.tree.insert("", "end", values=(
                    eq.get("ID_EQUIPAMENTO", ""),
                    eq.get("TIPO_EQUIPAMENTO", ""),
                    eq.get("NOME", ""),
                    eq.get("MARCA", ""),
                    eq.get("STATUS", ""),
                    eq.get("ESTADO_CONSERVACAO", "")
                ))
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar equipamentos:\n{e}")

    def abrir_formulario(self):
        form = tk.Toplevel(self.conteudo)
        form.title("Novo Equipamento - ProAgro Consultoria")
        form.geometry("700x620")
        form.config(bg="#F4F7F5")
        form.grab_set()

        tk.Label(form, text="Cadastrar Novo Equipamento", font=("Arial", 18, "bold"), fg="#173F2A", bg="#F4F7F5").pack(pady=(20, 10))

        container = tk.Frame(form, bg="#F4F7F5")
        container.pack(fill="both", expand=True, padx=20, pady=10)

        canvas = tk.Canvas(container, bg="#F4F7F5", highlightthickness=0)
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
        campos_frame = tk.Frame(canvas, bg="#F4F7F5")
        campos_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=campos_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Campos
        tk.Label(campos_frame, text="Tipo de Equipamento:", font=("Arial", 9, "bold"), bg="#F4F7F5").grid(row=0, column=0, sticky="w", pady=(5, 0))
        tk.Label(campos_frame, text="Nome *:", font=("Arial", 9, "bold"), bg="#F4F7F5").grid(row=0, column=1, sticky="w", pady=(5, 0), padx=(10, 0))

        tipo_combo = ttk.Combobox(campos_frame, values=["Trator", "Implemento", "Drone", "Veículo", "Ferramenta", "Outros"], state="readonly", font=("Arial", 10))
        tipo_combo.set("Trator")
        tipo_combo.grid(row=1, column=0, sticky="ew", pady=(0, 10))

        entry_nome = tk.Entry(campos_frame, font=("Arial", 10), relief="solid", bd=1)
        entry_nome.grid(row=1, column=1, sticky="ew", pady=(0, 10), padx=(10, 0), ipady=3)

        tk.Label(campos_frame, text="Marca:", font=("Arial", 9, "bold"), bg="#F4F7F5").grid(row=2, column=0, sticky="w", pady=(5, 0))
        tk.Label(campos_frame, text="Modelo:", font=("Arial", 9, "bold"), bg="#F4F7F5").grid(row=2, column=1, sticky="w", pady=(5, 0), padx=(10, 0))

        entry_marca = tk.Entry(campos_frame, font=("Arial", 10), relief="solid", bd=1)
        entry_marca.grid(row=3, column=0, sticky="ew", pady=(0, 10), ipady=3)

        entry_modelo = tk.Entry(campos_frame, font=("Arial", 10), relief="solid", bd=1)
        entry_modelo.grid(row=3, column=1, sticky="ew", pady=(0, 10), padx=(10, 0), ipady=3)

        tk.Label(campos_frame, text="Número de Série:", font=("Arial", 9, "bold"), bg="#F4F7F5").grid(row=4, column=0, sticky="w", pady=(5, 0))
        tk.Label(campos_frame, text="Patrimônio:", font=("Arial", 9, "bold"), bg="#F4F7F5").grid(row=4, column=1, sticky="w", pady=(5, 0), padx=(10, 0))

        entry_serie = tk.Entry(campos_frame, font=("Arial", 10), relief="solid", bd=1)
        entry_serie.grid(row=5, column=0, sticky="ew", pady=(0, 10), ipady=3)

        entry_patrimonio = tk.Entry(campos_frame, font=("Arial", 10), relief="solid", bd=1)
        entry_patrimonio.grid(row=5, column=1, sticky="ew", pady=(0, 10), padx=(10, 0), ipady=3)

        tk.Label(campos_frame, text="Status:", font=("Arial", 9, "bold"), bg="#F4F7F5").grid(row=6, column=0, sticky="w", pady=(5, 0))
        tk.Label(campos_frame, text="Estado de Conservação:", font=("Arial", 9, "bold"), bg="#F4F7F5").grid(row=6, column=1, sticky="w", pady=(5, 0), padx=(10, 0))

        status_combo = ttk.Combobox(campos_frame, values=["Disponível", "Em Uso", "Em Manutenção", "Baixado"], state="readonly", font=("Arial", 10))
        status_combo.set("Disponível")
        status_combo.grid(row=7, column=0, sticky="ew", pady=(0, 10))

        conservacao_combo = ttk.Combobox(campos_frame, values=["Excelente", "Bom", "Regular", "Ruim"], state="readonly", font=("Arial", 10))
        conservacao_combo.set("Bom")
        conservacao_combo.grid(row=7, column=1, sticky="ew", pady=(0, 10), padx=(10, 0))

        tk.Label(campos_frame, text="Data de Aquisição:", font=("Arial", 9, "bold"), bg="#F4F7F5").grid(row=8, column=0, sticky="w", pady=(5, 0))
        tk.Label(campos_frame, text="Valor de Aquisição (R$):", font=("Arial", 9, "bold"), bg="#F4F7F5").grid(row=8, column=1, sticky="w", pady=(5, 0), padx=(10, 0))

        entry_data_aq = tk.Entry(campos_frame, font=("Arial", 10), relief="solid", bd=1)
        entry_data_aq.grid(row=9, column=0, sticky="ew", pady=(0, 10), ipady=3)

        entry_valor_aq = tk.Entry(campos_frame, font=("Arial", 10), relief="solid", bd=1)
        entry_valor_aq.grid(row=9, column=1, sticky="ew", pady=(0, 10), padx=(10, 0), ipady=3)

        tk.Label(campos_frame, text="Localização:", font=("Arial", 9, "bold"), bg="#F4F7F5").grid(row=10, column=0, sticky="w", pady=(5, 0))
        tk.Label(campos_frame, text="Responsável:", font=("Arial", 9, "bold"), bg="#F4F7F5").grid(row=10, column=1, sticky="w", pady=(5, 0), padx=(10, 0))

        entry_local = tk.Entry(campos_frame, font=("Arial", 10), relief="solid", bd=1)
        entry_local.grid(row=11, column=0, sticky="ew", pady=(0, 10), ipady=3)

        entry_resp = tk.Entry(campos_frame, font=("Arial", 10), relief="solid", bd=1)
        entry_resp.grid(row=11, column=1, sticky="ew", pady=(0, 10), padx=(10, 0), ipady=3)

        tk.Label(campos_frame, text="Observações:", font=("Arial", 9, "bold"), bg="#F4F7F5").grid(row=12, column=0, columnspan=2, sticky="w", pady=(5, 0))
        entry_obs = tk.Entry(campos_frame, font=("Arial", 10), relief="solid", bd=1)
        entry_obs.grid(row=13, column=0, columnspan=2, sticky="ew", pady=(0, 15), ipady=3)

        def salvar():
            nome = entry_nome.get().strip()
            if not nome:
                messagebox.showwarning("Aviso", "O campo Nome é obrigatório!", parent=form)
                return
            try:
                novo_id = gerar_id_equipamento()
                dados = {
                    "ID_EQUIPAMENTO": novo_id,
                    "TIPO_EQUIPAMENTO": tipo_combo.get(),
                    "NOME": nome,
                    "MARCA": entry_marca.get().strip(),
                    "MODELO": entry_modelo.get().strip(),
                    "NUMERO_SERIE": entry_serie.get().strip(),
                    "PATRIMONIO": entry_patrimonio.get().strip(),
                    "STATUS": status_combo.get(),
                    "ESTADO_CONSERVACAO": conservacao_combo.get(),
                    "DATA_AQUISICAO": entry_data_aq.get().strip(),
                    "VALOR_AQUISICAO": entry_valor_aq.get().strip(),
                    "LOCALIZACAO": entry_local.get().strip(),
                    "RESPONSAVEL": entry_resp.get().strip(),
                    "OBSERVACOES": entry_obs.get().strip(),
                    "IMAGEM": "",
                    "DATA_CADASTRO": ""
                }
                adicionar_equipamento(dados)
                messagebox.showinfo("Sucesso", f"Equipamento {novo_id} cadastrado com sucesso!", parent=form)
                form.destroy()
                self.carregar_dados()
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao salvar:\n{e}", parent=form)

        btn_salvar = tk.Button(
            campos_frame, text="Salvar Equipamento", command=salvar,
            font=("Arial", 11, "bold"), fg="white", bg="#173F2A", relief="flat", pady=10, cursor="hand2"
        )
        btn_salvar.grid(row=14, column=0, columnspan=2, sticky="ew", pady=(10, 20))