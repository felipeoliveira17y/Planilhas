import tkinter as tk
from tkinter import messagebox, ttk
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))
from excel import ler_tabela, gerar_id_receita, adicionar_receita, gerar_id_despesa, adicionar_despesa


class TelaFinanceiro:

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

        titulo = tk.Label(topo, text="Financeiro", font=("Arial", 26, "bold"), fg="#173F2A", bg="#F4F7F5")
        titulo.pack(side="left")

        # Botões de Ação rápida no topo
        btn_despesa = tk.Button(
            topo, text="＋ NOVA DESPESA", command=self.abrir_formulario_despesa,
            font=("Arial", 10, "bold"), fg="white", bg="#A93226", relief="flat", padx=12, pady=10, cursor="hand2"
        )
        btn_despesa.pack(side="right", padx=(10, 0))

        btn_receita = tk.Button(
            topo, text="＋ NOVA RECEITA", command=self.abrir_formulario_receita,
            font=("Arial", 10, "bold"), fg="white", bg="#245C3E", relief="flat", padx=12, pady=10, cursor="hand2"
        )
        btn_receita.pack(side="right")

        # Notebook (Abas) para Receitas e Despesas
        abas_frame = ttk.Notebook(self.conteudo)
        abas_frame.pack(fill="both", expand=True, padx=40, pady=(0, 40))

        self.tab_receitas = tk.Frame(abas_frame, bg="#F4F7F5")
        self.tab_despesas = tk.Frame(abas_frame, bg="#F4F7F5")

        abas_frame.add(self.tab_receitas, text="  Receitas  ")
        abas_frame.add(self.tab_despesas, text="  Despesas  ")

        self.configurar_tabela_receitas()
        self.configurar_tabela_despesas()

    def configurar_tabela_receitas(self):
        colunas = ("ID", "CLIENTE", "DESCRICAO", "VALOR", "VENCIMENTO", "STATUS")
        self.tree_rec = ttk.Treeview(self.tab_receitas, columns=colunas, show="headings", selectmode="browse")

        self.tree_rec.heading("ID", text="ID")
        self.tree_rec.heading("CLIENTE", text="Cliente")
        self.tree_rec.heading("DESCRICAO", text="Descrição")
        self.tree_rec.heading("VALOR", text="Valor")
        self.tree_rec.heading("VENCIMENTO", text="Vencimento")
        self.tree_rec.heading("STATUS", text="Status")

        self.tree_rec.column("ID", width=90, anchor="w")
        self.tree_rec.column("CLIENTE", width=100, anchor="w")
        self.tree_rec.column("DESCRICAO", width=250, anchor="w")
        self.tree_rec.column("VALOR", width=110, anchor="w")
        self.tree_rec.column("VENCIMENTO", width=120, anchor="w")
        self.tree_rec.column("STATUS", width=110, anchor="w")

        scrollbar = ttk.Scrollbar(self.tab_receitas, orient="vertical", command=self.tree_rec.yview)
        self.tree_rec.configure(yscrollcommand=scrollbar.set)

        self.tree_rec.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        scrollbar.pack(side="right", fill="y", pady=10)

        for r in ler_tabela("tbReceitas"):
            val = f"R$ {r.get('VALOR', '')}" if r.get('VALOR') else ""
            self.tree_rec.insert("", "end", values=(
                r.get("ID_RECEITA", ""), r.get("ID_CLIENTE", ""), r.get("DESCRICAO", ""),
                val, r.get("DATA_VENCIMENTO", ""), r.get("STATUS", "")
            ))

    def configurar_tabela_despesas(self):
        colunas = ("ID", "CATEGORIA", "FORNECEDOR", "DESCRICAO", "VALOR", "VENCIMENTO", "STATUS")
        self.tree_desp = ttk.Treeview(self.tab_despesas, columns=colunas, show="headings", selectmode="browse")

        self.tree_desp.heading("ID", text="ID")
        self.tree_desp.heading("CATEGORIA", text="Categoria")
        self.tree_desp.heading("FORNECEDOR", text="Fornecedor")
        self.tree_desp.heading("DESCRICAO", text="Descrição")
        self.tree_desp.heading("VALOR", text="Valor")
        self.tree_desp.heading("VENCIMENTO", text="Vencimento")
        self.tree_desp.heading("STATUS", text="Status")

        self.tree_desp.column("ID", width=90, anchor="w")
        self.tree_desp.column("CATEGORIA", width=120, anchor="w")
        self.tree_desp.column("FORNECEDOR", width=130, anchor="w")
        self.tree_desp.column("DESCRICAO", width=180, anchor="w")
        self.tree_desp.column("VALOR", width=100, anchor="w")
        self.tree_desp.column("VENCIMENTO", width=110, anchor="w")
        self.tree_desp.column("STATUS", width=100, anchor="w")

        scrollbar = ttk.Scrollbar(self.tab_despesas, orient="vertical", command=self.tree_desp.yview)
        self.tree_desp.configure(yscrollcommand=scrollbar.set)

        self.tree_desp.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        scrollbar.pack(side="right", fill="y", pady=10)

        for d in ler_tabela("tbDespesas"):
            val = f"R$ {d.get('VALOR', '')}" if d.get('VALOR') else ""
            self.tree_desp.insert("", "end", values=(
                d.get("ID_DESPESA", ""), d.get("CATEGORIA", ""), d.get("FORNECEDOR", ""),
                d.get("DESCRICAO", ""), val, d.get("DATA_VENCIMENTO", ""), d.get("STATUS", "")
            ))

    def abrir_formulario_receita(self):
        form = tk.Toplevel(self.conteudo)
        form.title("Nova Receita - ProAgro Consultoria")
        form.geometry("650x550")
        form.config(bg="#F4F7F5")
        form.grab_set()

        tk.Label(form, text="Cadastrar Nova Receita", font=("Arial", 18, "bold"), fg="#173F2A", bg="#F4F7F5").pack(pady=(20, 10))

        container = tk.Frame(form, bg="#F4F7F5")
        container.pack(fill="both", expand=True, padx=20, pady=10)

        clientes = [f"{c.get('ID_CLIENTE')} - {c.get('NOME_RAZAO_SOCIAL')}" for c in ler_tabela("tbClientes") if c.get('ID_CLIENTE')]
        servicos = [f"{s.get('ID_SERVICO')} - {s.get('TIPO_SERVICO')}" for s in ler_tabela("tbServicos") if s.get('ID_SERVICO')]

        tk.Label(container, text="Cliente:", font=("Arial", 9, "bold"), bg="#F4F7F5").pack(anchor="w")
        cli_combo = ttk.Combobox(container, values=clientes, state="readonly", font=("Arial", 10), width=50)
        if clientes: cli_combo.set(clientes[0])
        cli_combo.pack(fill="x", pady=(0, 10))

        tk.Label(container, text="Serviço Vinculado:", font=("Arial", 9, "bold"), bg="#F4F7F5").pack(anchor="w")
        serv_combo = ttk.Combobox(container, values=servicos, state="readonly", font=("Arial", 10), width=50)
        if servicos: serv_combo.set(servicos[0])
        serv_combo.pack(fill="x", pady=(0, 10))

        tk.Label(container, text="Descrição:", font=("Arial", 9, "bold"), bg="#F4F7F5").pack(anchor="w")
        entry_desc = tk.Entry(container, font=("Arial", 10), relief="solid", bd=1)
        entry_desc.pack(fill="x", pady=(0, 10), ipady=3)

        tk.Label(container, text="Valor (R$):", font=("Arial", 9, "bold"), bg="#F4F7F5").pack(anchor="w")
        entry_val = tk.Entry(container, font=("Arial", 10), relief="solid", bd=1)
        entry_val.pack(fill="x", pady=(0, 10), ipady=3)

        tk.Label(container, text="Data de Vencimento:", font=("Arial", 9, "bold"), bg="#F4F7F5").pack(anchor="w")
        entry_venc = tk.Entry(container, font=("Arial", 10), relief="solid", bd=1)
        entry_venc.pack(fill="x", pady=(0, 10), ipady=3)

        tk.Label(container, text="Status:", font=("Arial", 9, "bold"), bg="#F4F7F5").pack(anchor="w")
        status_combo = ttk.Combobox(container, values=["Pendente", "Recebido", "Cancelado"], state="readonly", font=("Arial", 10))
        status_combo.set("Pendente")
        status_combo.pack(fill="x", pady=(0, 15))

        def salvar():
            try:
                id_cli = cli_combo.get().split(" - ")[0] if cli_combo.get() else ""
                id_serv = serv_combo.get().split(" - ")[0] if serv_combo.get() else ""
                novo_id = gerar_id_receita()
                dados = {
                    "ID_RECEITA": novo_id, "ID_CLIENTE": id_cli, "ID_SERVICO": id_serv,
                    "DESCRICAO": entry_desc.get().strip(), "VALOR": entry_val.get().strip(),
                    "DATA_EMISSAO": "", "DATA_VENCIMENTO": entry_venc.get().strip(),
                    "DATA_PAGAMENTO": "", "FORMA_PAGAMENTO": "", "STATUS": status_combo.get(), "OBSERVACOES": ""
                }
                adicionar_receita(dados)
                messagebox.showinfo("Sucesso", f"Receita {novo_id} salva!", parent=form)
                form.destroy()
                self.renderizar()
            except Exception as e:
                messagebox.showerror("Erro", f"Erro:\n{e}", parent=form)

        tk.Button(container, text="Salvar Receita", command=salvar, font=("Arial", 11, "bold"), fg="white", bg="#173F2A", relief="flat", pady=10, cursor="hand2").pack(fill="x")

    def abrir_formulario_despesa(self):
        form = tk.Toplevel(self.conteudo)
        form.title("Nova Despesa - ProAgro Consultoria")
        form.geometry("650x550")
        form.config(bg="#F4F7F5")
        form.grab_set()

        tk.Label(form, text="Cadastrar Nova Despesa", font=("Arial", 18, "bold"), fg="#A93226", bg="#F4F7F5").pack(pady=(20, 10))

        container = tk.Frame(form, bg="#F4F7F5")
        container.pack(fill="both", expand=True, padx=20, pady=10)

        tk.Label(container, text="Categoria:", font=("Arial", 9, "bold"), bg="#F4F7F5").pack(anchor="w")
        cat_combo = ttk.Combobox(container, values=["Operacional", "Combustível", "Manutenção", "Impostos", "Escritório", "Outros"], state="readonly", font=("Arial", 10))
        cat_combo.set("Operacional")
        cat_combo.pack(fill="x", pady=(0, 10))

        tk.Label(container, text="Fornecedor:", font=("Arial", 9, "bold"), bg="#F4F7F5").pack(anchor="w")
        entry_forn = tk.Entry(container, font=("Arial", 10), relief="solid", bd=1)
        entry_forn.pack(fill="x", pady=(0, 10), ipady=3)

        tk.Label(container, text="Descrição:", font=("Arial", 9, "bold"), bg="#F4F7F5").pack(anchor="w")
        entry_desc = tk.Entry(container, font=("Arial", 10), relief="solid", bd=1)
        entry_desc.pack(fill="x", pady=(0, 10), ipady=3)

        tk.Label(container, text="Valor (R$):", font=("Arial", 9, "bold"), bg="#F4F7F5").pack(anchor="w")
        entry_val = tk.Entry(container, font=("Arial", 10), relief="solid", bd=1)
        entry_val.pack(fill="x", pady=(0, 10), ipady=3)

        tk.Label(container, text="Data de Vencimento:", font=("Arial", 9, "bold"), bg="#F4F7F5").pack(anchor="w")
        entry_venc = tk.Entry(container, font=("Arial", 10), relief="solid", bd=1)
        entry_venc.pack(fill="x", pady=(0, 10), ipady=3)

        tk.Label(container, text="Status:", font=("Arial", 9, "bold"), bg="#F4F7F5").pack(anchor="w")
        status_combo = ttk.Combobox(container, values=["Pendente", "Pago", "Cancelado"], state="readonly", font=("Arial", 10))
        status_combo.set("Pendente")
        status_combo.pack(fill="x", pady=(0, 15))

        def salvar():
            try:
                novo_id = gerar_id_despesa()
                dados = {
                    "ID_DESPESA": novo_id, "CATEGORIA": cat_combo.get(), "DESCRICAO": entry_desc.get().strip(),
                    "FORNECEDOR": entry_forn.get().strip(), "VALOR": entry_val.get().strip(),
                    "DATA_LANCAMENTO": "", "DATA_VENCIMENTO": entry_venc.get().strip(),
                    "DATA_PAGAMENTO": "", "FORMA_PAGAMENTO": "", "STATUS": status_combo.get(), "OBSERVACOES": ""
                }
                adicionar_despesa(dados)
                messagebox.showinfo("Sucesso", f"Despesa {novo_id} salva!", parent=form)
                form.destroy()
                self.renderizar()
            except Exception as e:
                messagebox.showerror("Erro", f"Erro:\n{e}", parent=form)

        tk.Button(container, text="Salvar Despesa", command=salvar, font=("Arial", 11, "bold"), fg="white", bg="#A93226", relief="flat", pady=10, cursor="hand2").pack(fill="x")