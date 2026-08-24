import os
import tkinter as tk
from PIL import Image, ImageTk
from excel import ler_tabela


class Dashboard:

    def __init__(self, root):
        self.root = root
        self.root.title("Landmensure - Sistema de Gestão")
        self.root.geometry("1200x700")
        self.root.minsize(1000, 600)

        # Paleta de Cores (Laranja e Preto Moderno)
        self.cor_menu = "#161616"
        self.cor_laranja = "#FF6600"
        self.cor_hover = "#2A2A2A"
        self.cor_conteudo = "#F4F7F5"

        # Estado da bandeja (False = recolhida, True = expandida)
        self.menu_expandido = False

        self.criar_interface()

    def criar_interface(self):
        # ==============================
        # MENU LATERAL (BANDEJA RECOLHÍVEL)
        # ==============================
        self.menu = tk.Frame(
            self.root,
            bg=self.cor_menu,
            width=70
        )
        self.menu.pack(side="left", fill="y")
        self.menu.pack_propagate(False)

        # Topo do Menu: Botão Animado de Expandir/Recolher
        topo_menu = tk.Frame(self.menu, bg=self.cor_menu, height=60)
        topo_menu.pack(fill="x", pady=10)

        self.btn_toggle = tk.Button(
            topo_menu,
            text="≡",  # Símbolo refinado para o menu
            command=self.alternar_menu,
            font=("Arial", 18, "bold"),
            fg="white",
            bg=self.cor_menu,
            activebackground=self.cor_menu,
            activeforeground=self.cor_laranja,
            relief="flat",
            bd=0,
            cursor="hand2",
            width=3
        )
        self.btn_toggle.pack(side="left", padx=10)

        # Container dos Botões
        self.botoes_container = tk.Frame(self.menu, bg=self.cor_menu)
        self.botoes_container.pack(fill="both", expand=True, pady=10)

        # Lista de menus
        self.botoes_info = [
            ("home.png", "Início", self.inicio),
            ("clientes.png", "Clientes", self.clientes),
            ("propriedades.png", "Propriedades", self.propriedades),
            ("servicos.png", "Serviços", self.servicos),
            ("equipamentos.png", "Equipamentos", self.equipamentos),
            ("financeiro.png", "Financeiro", self.financeiro),
            ("documentos.png", "Documentos", self.documentos),
            ("relatorios.png", "Relatórios", self.relatorios),
        ]

        self.botoes_criados = []
        for arquivo_icone, texto, comando in self.botoes_info:
            btn_frame = self.criar_botao_lateral(arquivo_icone, texto, comando)
            self.botoes_criados.append(btn_frame)

        # ==============================
        # ÁREA PRINCIPAL
        # ==============================
        self.conteudo = tk.Frame(
            self.root,
            bg=self.cor_conteudo
        )
        self.conteudo.pack(side="right", fill="both", expand=True)

        self.inicio()

    def criar_botao_lateral(self, arquivo_icone, texto, comando):
        # Frame individual para o botão (simula um componente unificado com ícone fixo + texto dinâmico)
        btn_frame = tk.Frame(self.botoes_container, bg=self.cor_menu, cursor="hand2")
        btn_frame.pack(fill="x", pady=6, padx=8)

        caminho_img = os.path.join("icons", arquivo_icone)
        imagem_tk = None
        if os.path.exists(caminho_img):
            try:
                img = Image.open(caminho_img).convert("RGBA")
                dados = img.getdata()
                novos_dados = []
                for item in dados:
                    if item[0] < 50 and item[1] < 50 and item[2] < 50:
                        novos_dados.append((255, 255, 255, item[3]))
                    else:
                        novos_dados.append(item)
                img.putdata(novos_dados)
                
                img = img.resize((22, 22), Image.Resampling.LANCZOS)
                imagem_tk = ImageTk.PhotoImage(img)
            except Exception as e:
                print(f"Erro ao processar ícone {arquivo_icone}: {e}")

        # Ícone Fixo (Label independente para não se mover)
        lbl_icone = tk.Label(btn_frame, bg=self.cor_menu, cursor="hand2")
        if imagem_tk:
            lbl_icone.image = imagem_tk
            lbl_icone.config(image=imagem_tk)
        lbl_icone.pack(side="left", padx=12, pady=10)

        # Texto Dinâmico (Label que aparece apenas quando expandido)
        lbl_texto = tk.Label(
            btn_frame,
            text=texto,
            font=("Arial", 11),
            fg="#CCCCCC",
            bg=self.cor_menu,
            anchor="w",
            cursor="hand2"
        )
        # Inicialmente recolhido (texto oculto)
        # Não damos .pack() no texto agora para ele ficar invisível na largura de 70px

        # Guardamos referências úteis no frame
        btn_frame.lbl_texto = lbl_texto
        btn_frame.lbl_icone = lbl_icone

        # Eventos de Clique e Hover para todo o Frame e seus filhos
        for widget in (btn_frame, lbl_icone, lbl_texto):
            widget.bind("<Button-1>", lambda e: comando())
            widget.bind("<Enter>", lambda e: self.aplicar_hover(btn_frame, True))
            widget.bind("<Leave>", lambda e: self.aplicar_hover(btn_frame, False))

        return btn_frame

    def aplicar_hover(self, frame, entrar):
        cor = self.cor_hover if entrar else self.cor_menu
        cor_txt = self.cor_laranja if entrar else "#CCCCCC"
        
        frame.config(bg=cor)
        frame.lbl_icone.config(bg=cor)
        frame.lbl_texto.config(bg=cor, fg=cor_txt)

    def alternar_menu(self):
        """Expande ou recolhe a bandeja lateral com animação fluida no ícone hambúrguer"""
        if self.menu_expandido:
            # Recolher
            self.menu.config(width=70)
            self.btn_toggle.config(text="≡") # Ícone recolhido
            for frame in self.botoes_criados:
                frame.lbl_texto.pack_forget() # Esconde o texto
            self.menu_expandido = False
        else:
            # Expandir
            self.menu.config(width=220)
            self.btn_toggle.config(text="‹") # Ícone animado indicando recolhimento
            for frame in self.botoes_criados:
                frame.lbl_texto.pack(side="left", padx=(0, 10), fill="x", expand=True) # Mostra o texto fluido
            self.menu_expandido = True

    # ==================================
    # PÁGINAS E CARDS
    # ==================================

    def limpar_conteudo(self):
        for widget in self.conteudo.winfo_children():
            widget.destroy()

    def inicio(self):
        self.limpar_conteudo()

        titulo = tk.Label(
            self.conteudo,
            text="Dashboard",
            font=("Arial", 26, "bold"),
            fg="#1A1A1A",
            bg=self.cor_conteudo
        )
        titulo.pack(anchor="w", padx=40, pady=(35, 5))

        subtitulo = tk.Label(
            self.conteudo,
            text="Visão geral do sistema Landmensure",
            font=("Arial", 11),
            fg="#666666",
            bg=self.cor_conteudo
        )
        subtitulo.pack(anchor="w", padx=40)

        # Lendo os dados reais do Excel com segurança
        try:
            total_clientes = str(len(ler_tabela("tbClientes") or []))
        except:
            total_clientes = "0"

        try:
            total_servicos = str(len(ler_tabela("tbServicos") or []))
        except:
            total_servicos = "0"

        try:
            total_equipamentos = str(len(ler_tabela("tbEquipamentos") or []))
        except:
            total_equipamentos = "0"

        try:
            total_documentos = str(len(ler_tabela("tbDocumentos") or []))
        except:
            total_documentos = "0"

        cards = tk.Frame(self.conteudo, bg=self.cor_conteudo)
        cards.pack(fill="x", padx=40, pady=35)

        self.criar_card(cards, "CLIENTES", total_clientes, 0)
        self.criar_card(cards, "SERVIÇOS", total_servicos, 1)
        self.criar_card(cards, "EQUIPAMENTOS", total_equipamentos, 2)
        self.criar_card(cards, "DOCUMENTOS", total_documentos, 3)
            
    def criar_card(self, parent, titulo, valor, coluna):
        card = tk.Frame(
            parent,
            bg="white",
            width=190,
            height=120,
            highlightbackground="#E0E0E0",
            highlightthickness=1
        )
        card.grid(row=0, column=coluna, padx=8, sticky="nsew")
        parent.grid_columnconfigure(coluna, weight=1)
        card.pack_propagate(False)

        # Detalhe laranja no topo do card
        barra = tk.Frame(card, bg=self.cor_laranja, height=4)
        barra.pack(fill="x", side="top")

        tk.Label(
            card,
            text=titulo,
            font=("Arial", 9, "bold"),
            fg="#777777",
            bg="white"
        ).pack(anchor="w", padx=18, pady=(14, 5))

        tk.Label(
            card,
            text=valor,
            font=("Arial", 26, "bold"),
            fg="#1A1A1A",
            bg="white"
        ).pack(anchor="w", padx=18)

    # ==================================
    # MÓDULOS DE NAVEGAÇÃO
    # ==================================

    def clientes(self, *args):
        self.limpar_conteudo()
        from interface.clientes import TelaClientes
        TelaClientes(self.conteudo, self)

    def propriedades(self, *args):
        self.limpar_conteudo()
        from interface.propriedades import TelaPropriedades
        TelaPropriedades(self.conteudo, self)

    def servicos(self, *args):
        self.limpar_conteudo()
        from interface.servicos import TelaServicos
        TelaServicos(self.conteudo, self)

    def equipamentos(self, *args):
        self.limpar_conteudo()
        from interface.equipamentos import TelaEquipamentos
        TelaEquipamentos(self.conteudo, self)

    def financeiro(self, *args):
        self.limpar_conteudo()
        from interface.financeiro import TelaFinanceiro
        TelaFinanceiro(self.conteudo, self)

    def documentos(self, *args):
        self.limpar_conteudo()
        from interface.documentos import TelaDocumentos
        TelaDocumentos(self.conteudo, self)

    def relatorios(self, *args):
        self.limpar_conteudo()
        from interface.relatorios import TelaRelatorios
        TelaRelatorios(self.conteudo, self)