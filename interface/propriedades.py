import tkinter as tk
from tkinter import messagebox, ttk
import sys
from pathlib import Path

# Adiciona a raiz do projeto ao path para importar o excel corretamente
sys.path.append(str(Path(__file__).parent.parent))

from excel import ler_tabela, gerar_id_propriedade, adicionar_propriedade


class TelaPropriedades:

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
            text="Propriedades",
            font=("Arial", 26, "bold"),
            fg="#173F2A",
            bg="#F4F7F5"
        )
        titulo.pack(side="left")

        btn_novo = tk.Button(
            topo,
            text="＋ NOVA PROPRIEDADE",
            command=self.abrir_formulario_nova_propriedade,
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
        # TABELA / LISTAGEM DE PROPRIEDADES
        # ==============================
        tabela_frame = tk.Frame(self.conteudo, bg="#F4F7F5")
        tabela_frame.pack(fill="both", expand=True, padx=40, pady=(0, 40))

        colunas = ("ID_PROP", "CLIENTE", "NOME", "TIPO", "MUNICIPIO", "AREA")
        
        self.tree = ttk.Treeview(
            tabela_frame,
            columns=colunas,
            show="headings",
            selectmode="browse"
        )

        self.tree.heading("ID_PROP", text="ID Propriedade")
        self.tree.heading("CLIENTE", text="ID Cliente")
        self.tree.heading("NOME", text="Nome da Propriedade")
        self.tree.heading("TIPO", text="Tipo")
        self.tree.heading("MUNICIPIO", text="Cidade/UF")
        self.tree.heading("AREA", text="Área Total")

        self.tree.column("ID_PROP", width=110, anchor="w")
        self.tree.column("CLIENTE", width=100, anchor="w")
        self.tree.column("NOME", width=250, anchor="w")
        self.tree.column("TIPO", width=130, anchor="w")
        self.tree.column("MUNICIPIO", width=130, anchor="w")
        self.tree.column("AREA", width=100, anchor="w")

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
            propriedades = ler_tabela("tbPropriedades")
            for p in propriedades:
                area_formatada = f"{p.get('AREA_TOTAL', '')} {p.get('UNIDADE_AREA', '')}".strip()
                cidade_uf = f"{p.get('CIDADE', '')}/{p.get('UF', '')}".strip("/")
                self.tree.insert(
                    "",
                    "end",
                    values=(
                        p.get("ID_PROPRIEDADE", ""),
                        p.get("ID_CLIENTE", ""),
                        p.get("NOME_PROPRIEDADE", ""),
                        p.get("TIPO_PROPRIEDADE", ""),
                        cidade_uf,
                        area_formatada
                    )
                )
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar propriedades do Excel:\n{e}")

    def abrir_formulario_nova_propriedade(self):
        # Janela Toplevel com scroll para o formulário de propriedades
        form = tk.Toplevel(self.conteudo)
        form.title("Nova Propriedade - ProAgro Consultoria")
        form.geometry("750x680")
        form.config(bg="#F4F7F5")
        form.grab_set()

        tk.Label(
            form,
            text="Cadastrar Nova Propriedade",
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

        # Buscar lista de clientes cadastrados para popular o combobox de vínculo
        clientes_cadastrados = []
        try:
            dados_clientes = ler_tabela("tbClientes")
            for c in dados_clientes:
                id_c = c.get("ID_CLIENTE", "")
                nome_c = c.get("NOME_RAZAO_SOCIAL", "")
                if id_c:
                    clientes_cadastrados.append(f"{id_c} - {nome_c}")
        except:
            pass

        # ==========================================
        # CONSTRUÇÃO DOS CAMPOS (GRID DE 2 COLUNAS)
        # ==========================================
        
        # Linha 0: Cliente e Tipo de Propriedade
        tk.Label(campos_frame, text="Vincular ao Cliente *:", font=("Arial", 9, "bold"), bg="#F4F7F5", fg="#333").grid(row=0, column=0, sticky="w", pady=(5, 0))
        tk.Label(campos_frame, text="Tipo de Propriedade:", font=("Arial", 9, "bold"), bg="#F4F7F5", fg="#333").grid(row=0, column=1, sticky="w", pady=(5, 0), padx=(10, 0))

        cliente_combo = ttk.Combobox(campos_frame, values=clientes_cadastrados, state="readonly", font=("Arial", 10), width=35)
        if clientes_cadastrados:
            cliente_combo.set(clientes_cadastrados[0])
        cliente_combo.grid(row=1, column=0, sticky="ew", pady=(0, 10))

        tipo_prop_combo = ttk.Combobox(campos_frame, values=["Fazenda", "Sítio", "Chácara", "Área Rural", "Outros"], state="readonly", font=("Arial", 10), width=25)
        tipo_prop_combo.set("Fazenda")
        tipo_prop_combo.grid(row=1, column=1, sticky="ew", pady=(0, 10), padx=(10, 0))

        # Linha 1: Nome da Propriedade e CAR
        tk.Label(campos_frame, text="Nome da Propriedade *:", font=("Arial", 9, "bold"), bg="#F4F7F5", fg="#333").grid(row=2, column=0, sticky="w", pady=(5, 0))
        tk.Label(campos_frame, text="CAR (Cadastro Ambiental Rural):", font=("Arial", 9, "bold"), bg="#F4F7F5", fg="#333").grid(row=2, column=1, sticky="w", pady=(5, 0), padx=(10, 0))

        entry_nome_prop = tk.Entry(campos_frame, font=("Arial", 10), relief="solid", bd=1, width=38)
        entry_nome_prop.grid(row=3, column=0, sticky="ew", pady=(0, 10), ipady=3)

        entry_car = tk.Entry(campos_frame, font=("Arial", 10), relief="solid", bd=1)
        entry_car.grid(row=3, column=1, sticky="ew", pady=(0, 10), padx=(10, 0), ipady=3)

        # Linha 2: CCIR e INCRA
        tk.Label(campos_frame, text="CCIR:", font=("Arial", 9, "bold"), bg="#F4F7F5", fg="#333").grid(row=4, column=0, sticky="w", pady=(5, 0))
        tk.Label(campos_frame, text="INCRA:", font=("Arial", 9, "bold"), bg="#F4F7F5", fg="#333").grid(row=4, column=1, sticky="w", pady=(5, 0), padx=(10, 0))

        entry_ccir = tk.Entry(campos_frame, font=("Arial", 10), relief="solid", bd=1)
        entry_ccir.grid(row=5, column=0, sticky="ew", pady=(0, 10), ipady=3)

        entry_incra = tk.Entry(campos_frame, font=("Arial", 10), relief="solid", bd=1)
        entry_incra.grid(row=5, column=1, sticky="ew", pady=(0, 10), padx=(10, 0), ipady=3)

        # Linha 3: Área Total e Unidade de Área
        tk.Label(campos_frame, text="Área Total:", font=("Arial", 9, "bold"), bg="#F4F7F5", fg="#333").grid(row=6, column=0, sticky="w", pady=(5, 0))
        tk.Label(campos_frame, text="Unidade de Área:", font=("Arial", 9, "bold"), bg="#F4F7F5", fg="#333").grid(row=6, column=1, sticky="w", pady=(5, 0), padx=(10, 0))

        entry_area = tk.Entry(campos_frame, font=("Arial", 10), relief="solid", bd=1)
        entry_area.grid(row=7, column=0, sticky="ew", pady=(0, 10), ipady=3)

        unidade_combo = ttk.Combobox(campos_frame, values=["Hectares (ha)", "Alqueires", "Alqueires Paulista", "Alqueires Mineiro", "m²"], state="readonly", font=("Arial", 10))
        unidade_combo.set("Hectares (ha)")
        unidade_combo.grid(row=7, column=1, sticky="ew", pady=(0, 10), padx=(10, 0))

        # Linha 4: Latitude e Longitude
        tk.Label(campos_frame, text="Latitude:", font=("Arial", 9, "bold"), bg="#F4F7F5", fg="#333").grid(row=8, column=0, sticky="w", pady=(5, 0))
        tk.Label(campos_frame, text="Longitude:", font=("Arial", 9, "bold"), bg="#F4F7F5", fg="#333").grid(row=8, column=1, sticky="w", pady=(5, 0), padx=(10, 0))

        entry_lat = tk.Entry(campos_frame, font=("Arial", 10), relief="solid", bd=1)
        entry_lat.grid(row=9, column=0, sticky="ew", pady=(0, 10), ipady=3)

        entry_long = tk.Entry(campos_frame, font=("Arial", 10), relief="solid", bd=1)
        entry_long.grid(row=9, column=1, sticky="ew", pady=(0, 10), padx=(10, 0), ipady=3)

        # Linha 5: CEP e Endereço
        tk.Label(campos_frame, text="CEP:", font=("Arial", 9, "bold"), bg="#F4F7F5", fg="#333").grid(row=10, column=0, sticky="w", pady=(5, 0))
        tk.Label(campos_frame, text="Endereço / Localidade:", font=("Arial", 9, "bold"), bg="#F4F7F5", fg="#333").grid(row=10, column=1, sticky="w", pady=(5, 0), padx=(10, 0))

        entry_cep = tk.Entry(campos_frame, font=("Arial", 10), relief="solid", bd=1)
        entry_cep.grid(row=11, column=0, sticky="ew", pady=(0, 10), ipady=3)

        entry_endereco = tk.Entry(campos_frame, font=("Arial", 10), relief="solid", bd=1)
        entry_endereco.grid(row=11, column=1, sticky="ew", pady=(0, 10), padx=(10, 0), ipady=3)

        # Linha 6: Número e Complemento
        tk.Label(campos_frame, text="Número:", font=("Arial", 9, "bold"), bg="#F4F7F5", fg="#333").grid(row=12, column=0, sticky="w", pady=(5, 0))
        tk.Label(campos_frame, text="Complemento:", font=("Arial", 9, "bold"), bg="#F4F7F5", fg="#333").grid(row=12, column=1, sticky="w", pady=(5, 0), padx=(10, 0))

        entry_numero = tk.Entry(campos_frame, font=("Arial", 10), relief="solid", bd=1)
        entry_numero.grid(row=13, column=0, sticky="ew", pady=(0, 10), ipady=3)

        entry_complemento = tk.Entry(campos_frame, font=("Arial", 10), relief="solid", bd=1)
        entry_complemento.grid(row=13, column=1, sticky="ew", pady=(0, 10), padx=(10, 0), ipady=3)

        # Linha 7: Bairro e Cidade
        tk.Label(campos_frame, text="Bairro / Distrito:", font=("Arial", 9, "bold"), bg="#F4F7F5", fg="#333").grid(row=14, column=0, sticky="w", pady=(5, 0))
        tk.Label(campos_frame, text="Cidade:", font=("Arial", 9, "bold"), bg="#F4F7F5", fg="#333").grid(row=14, column=1, sticky="w", pady=(5, 0), padx=(10, 0))

        entry_bairro = tk.Entry(campos_frame, font=("Arial", 10), relief="solid", bd=1)
        entry_bairro.grid(row=15, column=0, sticky="ew", pady=(0, 10), ipady=3)

        entry_cidade = tk.Entry(campos_frame, font=("Arial", 10), relief="solid", bd=1)
        entry_cidade.grid(row=15, column=1, sticky="ew", pady=(0, 10), padx=(10, 0), ipady=3)

        # Linha 8: UF
        tk.Label(campos_frame, text="UF (Estado):", font=("Arial", 9, "bold"), bg="#F4F7F5", fg="#333").grid(row=16, column=0, sticky="w", pady=(5, 0))
        entry_uf = tk.Entry(campos_frame, font=("Arial", 10), relief="solid", bd=1)
        entry_uf.grid(row=17, column=0, sticky="ew", pady=(0, 10), ipady=3)

        # Linha 9: Observações
        tk.Label(campos_frame, text="Observações:", font=("Arial", 9, "bold"), bg="#F4F7F5", fg="#333").grid(row=18, column=0, columnspan=2, sticky="w", pady=(5, 0))
        entry_obs = tk.Entry(campos_frame, font=("Arial", 10), relief="solid", bd=1)
        entry_obs.grid(row=19, column=0, columnspan=2, sticky="ew", pady=(0, 15), ipady=3)

        # ==========================================
        # BOTÃO SALVAR
        # ==========================================
        def salvar():
            nome_prop = entry_nome_prop.get().strip()
            if not nome_prop:
                messagebox.showwarning("Aviso", "O campo Nome da Propriedade é obrigatório!", parent=form)
                return

            cliente_selecionado = cliente_combo.get()
            if not cliente_selecionado:
                messagebox.showwarning("Aviso", "Você precisa selecionar um cliente para vincular à propriedade!", parent=form)
                return

            # Extrai apenas o ID do cliente (ex: "CLI-001 - Nome" vira "CLI-001")
            id_cliente_extraido = cliente_selecionado.split(" - ")[0]

            try:
                # 1. Gera ID automático da propriedade
                novo_id_prop = gerar_id_propriedade()

                # 2. Monta o dicionário mapeando exatamente com a tbPropriedades
                dados = {
                    "ID_PROPRIEDADE": novo_id_prop,
                    "ID_CLIENTE": id_cliente_extraido,
                    "TIPO_PROPRIEDADE": tipo_prop_combo.get(),
                    "NOME_PROPRIEDADE": nome_prop,
                    "CAR": entry_car.get().strip(),
                    "CCIR": entry_ccir.get().strip(),
                    "INCRA": entry_incra.get().strip(),
                    "CEP": entry_cep.get().strip(),
                    "ENDERECO": entry_endereco.get().strip(),
                    "NUMERO": entry_numero.get().strip(),
                    "COMPLEMENTO": entry_complemento.get().strip(),
                    "BAIRRO": entry_bairro.get().strip(),
                    "CIDADE": entry_cidade.get().strip(),
                    "UF": entry_uf.get().strip().upper(),
                    "AREA_TOTAL": entry_area.get().strip(),
                    "UNIDADE_AREA": unidade_combo.get(),
                    "LATITUDE": entry_lat.get().strip(),
                    "LONGITUDE": entry_long.get().strip(),
                    "OBSERVACOES": entry_obs.get().strip(),
                    "DATA_CADASTRO": "",
                    "ATIVA": "SIM"
                }

                # 3. Salva no Excel
                adicionar_propriedade(dados)

                messagebox.showinfo("Sucesso", f"Propriedade {novo_id_prop} cadastrada e salva no Excel com sucesso!", parent=form)
                
                form.destroy()
                self.carregar_dados()

            except Exception as e:
                messagebox.showerror("Erro", f"Ocorreu um erro ao salvar a propriedade:\n{e}", parent=form)

        btn_salvar = tk.Button(
            campos_frame,
            text="Salvar Propriedade",
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
        btn_salvar.grid(row=20, column=0, columnspan=2, sticky="ew", pady=(10, 20))