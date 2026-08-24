import tkinter as tk
from tkinter import messagebox, ttk, filedialog
import sys
from pathlib import Path
import shutil

sys.path.append(str(Path(__file__).parent.parent))
from excel import ler_tabela, gerar_id_documento, adicionar_documento


class TelaDocumentos:

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

        titulo = tk.Label(topo, text="Documentos", font=("Arial", 26, "bold"), fg="#173F2A", bg="#F4F7F5")
        titulo.pack(side="left")

        btn_novo = tk.Button(
            topo, text="＋ NOVO DOCUMENTO", command=self.abrir_formulario,
            font=("Arial", 10, "bold"), fg="white", bg="#245C3E", relief="flat", padx=15, pady=10, cursor="hand2"
        )
        btn_novo.pack(side="right")
        # No método renderizar(), adicione o botão ao lado do "NOVO DOCUMENTO":
        btn_abrir = tk.Button(
            topo, text="📄 ABRIR ARQUIVO", command=self.abrir_arquivo_selecionado,
            font=("Arial", 10, "bold"), fg="white", bg="#2980B9", relief="flat", padx=15, pady=10, cursor="hand2"
        )
        btn_abrir.pack(side="right", padx=(0, 10))

        tabela_frame = tk.Frame(self.conteudo, bg="#F4F7F5")
        tabela_frame.pack(fill="both", expand=True, padx=40, pady=(0, 40))

        colunas = ("ID", "CLIENTE", "TIPO", "NUMERO", "VALIDADE")
        self.tree = ttk.Treeview(tabela_frame, columns=colunas, show="headings", selectmode="browse")

        self.tree.heading("ID", text="ID")
        self.tree.heading("CLIENTE", text="ID Cliente")
        self.tree.heading("TIPO", text="Tipo de Documento")
        self.tree.heading("NUMERO", text="Número")
        self.tree.heading("VALIDADE", text="Validade")

        self.tree.column("ID", width=100, anchor="w")
        self.tree.column("CLIENTE", width=110, anchor="w")
        self.tree.column("TIPO", width=220, anchor="w")
        self.tree.column("NUMERO", width=150, anchor="w")
        self.tree.column("VALIDADE", width=120, anchor="w")

        scrollbar = ttk.Scrollbar(tabela_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.carregar_dados()

    def abrir_arquivo_selecionado(self):
        selecionado = self.tree.selection()
        if not selecionado:
            messagebox.showwarning("Aviso", "Selecione um documento na tabela para abrir.")
            return
        
        item = self.tree.item(selecionado)
        id_doc = item["values"][0]

        # Procura o caminho do arquivo no Excel
        try:
            documentos = ler_tabela("tbDocumentos")
            caminho = ""
            for doc in documentos:
                if doc.get("ID_DOCUMENTO") == id_doc:
                    caminho = doc.get("CAMINHO_ARQUIVO")
                    break
            
            if caminho and Path(caminho).exists():
                import os
                os.startfile(caminho) # Abre o arquivo com o programa padrão do Windows
            else:
                messagebox.showerror("Erro", "O arquivo físico não foi encontrado ou não foi anexado.")
        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível abrir o arquivo:\n{e}")

    def carregar_dados(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        try:
            for doc in ler_tabela("tbDocumentos"):
                self.tree.insert("", "end", values=(
                    doc.get("ID_DOCUMENTO", ""),
                    doc.get("ID_CLIENTE", ""),
                    doc.get("TIPO_DOCUMENTO", ""),
                    doc.get("NUMERO_DOCUMENTO", ""),
                    doc.get("DATA_VALIDADE", "")
                ))
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar documentos:\n{e}")

    def abrir_formulario(self):
        form = tk.Toplevel(self.conteudo)
        form.title("Novo Documento - ProAgro Consultoria")
        form.geometry("650x580")
        form.config(bg="#F4F7F5")
        form.grab_set()

        tk.Label(form, text="Cadastrar Novo Documento", font=("Arial", 18, "bold"), fg="#173F2A", bg="#F4F7F5").pack(pady=(20, 10))

        container = tk.Frame(form, bg="#F4F7F5")
        container.pack(fill="both", expand=True, padx=20, pady=10)

        clientes = [f"{c.get('ID_CLIENTE')} - {c.get('NOME_RAZAO_SOCIAL')}" for c in ler_tabela("tbClientes") if c.get('ID_CLIENTE')]
        propriedades = [f"{p.get('ID_PROPRIEDADE')} - {p.get('NOME_PROPRIEDADE')}" for p in ler_tabela("tbPropriedades") if p.get('ID_PROPRIEDADE')]

        tk.Label(container, text="Cliente Vinculado *:", font=("Arial", 9, "bold"), bg="#F4F7F5").pack(anchor="w")
        cli_combo = ttk.Combobox(container, values=clientes, state="readonly", font=("Arial", 10), width=50)
        if clientes: cli_combo.set(clientes[0])
        cli_combo.pack(fill="x", pady=(0, 10))

        tk.Label(container, text="Propriedade Vinculada:", font=("Arial", 9, "bold"), bg="#F4F7F5").pack(anchor="w")
        prop_combo = ttk.Combobox(container, values=propriedades, state="readonly", font=("Arial", 10), width=50)
        if propriedades: prop_combo.set(propriedades[0])
        prop_combo.pack(fill="x", pady=(0, 10))

        tk.Label(container, text="Tipo de Documento *:", font=("Arial", 9, "bold"), bg="#F4F7F5").pack(anchor="w")
        tipo_combo = ttk.Combobox(container, values=["CAR", "CCIR", "INCRA", "Contrato", "Licença Ambiental", "Outros"], state="readonly", font=("Arial", 10))
        tipo_combo.set("CAR")
        tipo_combo.pack(fill="x", pady=(0, 10))

        tk.Label(container, text="Número do Documento:", font=("Arial", 9, "bold"), bg="#F4F7F5").pack(anchor="w")
        entry_num = tk.Entry(container, font=("Arial", 10), relief="solid", bd=1)
        entry_num.pack(fill="x", pady=(0, 10), ipady=3)

        tk.Label(container, text="Validade:", font=("Arial", 9, "bold"), bg="#F4F7F5").pack(anchor="w")
        entry_val = tk.Entry(container, font=("Arial", 10), relief="solid", bd=1)
        entry_val.pack(fill="x", pady=(0, 10), ipady=3)

        caminho_arquivo_var = tk.StringVar()
        tk.Label(container, text="Arquivo Anexo:", font=("Arial", 9, "bold"), bg="#F4F7F5").pack(anchor="w")
        
        def procurar_arquivo():
            filename = filedialog.askopenfilename(title="Selecionar Documento")
            if filename:
                caminho_arquivo_var.set(filename)

        btn_arq = tk.Button(container, text="Selecionar Arquivo...", command=procurar_arquivo, font=("Arial", 9), cursor="hand2")
        btn_arq.pack(anchor="w", pady=(0, 5))

        tk.Label(container, textvariable=caminho_arquivo_var, font=("Arial", 8), fg="#555", bg="#F4F7F5").pack(anchor="w", pady=(0, 10))

        def salvar():
            id_cli = cli_combo.get().split(" - ")[0] if cli_combo.get() else ""
            if not id_cli:
                messagebox.showwarning("Aviso", "Selecione um cliente!", parent=form)
                return

            try:
                novo_id = gerar_id_documento()
                arq_origem = caminho_arquivo_var.get()
                caminho_final = ""

                # Se um arquivo foi selecionado, copia ele para a pasta do sistema
                if arq_origem:
                    pasta_docs = Path("documentos_salvos")
                    pasta_docs.mkdir(exist_ok=True)
                    
                    # Pega a extensão do arquivo original (ex: .pdf, .jpg, .png)
                    extensao = Path(arq_origem).suffix
                    nome_novo_arquivo = f"{novo_id}_{id_cli}{extensao}"
                    caminho_destino = pasta_docs / nome_novo_arquivo
                    
                    shutil.copy(arq_origem, caminho_destino)
                    caminho_final = str(caminho_destino)

                dados = {
                    "ID_DOCUMENTO": novo_id,
                    "ID_CLIENTE": id_cli,
                    "ID_PROPRIEDADE": prop_combo.get().split(" - ")[0] if prop_combo.get() else "",
                    "TIPO_DOCUMENTO": tipo_combo.get(),
                    "NUMERO_DOCUMENTO": entry_num.get().strip(),
                    "DESCRICAO": "",
                    "DATA_EMISSAO": "",
                    "DATA_VALIDADE": entry_val.get().strip(),
                    "CAMINHO_ARQUIVO": caminho_final,
                    "OBSERVACOES": "",
                    "DATA_CADASTRO": ""
                }
                adicionar_documento(dados)
                messagebox.showinfo("Sucesso", f"Documento {novo_id} salvo e arquivo armazenado com sucesso!", parent=form)
                form.destroy()
                self.carregar_dados()
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao salvar:\n{e}", parent=form)