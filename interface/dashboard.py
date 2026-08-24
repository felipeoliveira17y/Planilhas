import tkinter as tk


class Dashboard:

    def __init__(self, root):

        self.root = root

        self.root.title(
            "ProAgro Consultoria - Sistema de Gestão"
        )

        self.root.geometry(
            "1200x700"
        )

        self.root.minsize(
            1000,
            600
        )

        self.criar_interface()

    def criar_interface(self):

        # ==============================
        # MENU LATERAL
        # ==============================

        self.menu = tk.Frame(
            self.root,
            bg="#173F2A",
            width=230
        )

        self.menu.pack(
            side="left",
            fill="y"
        )

        self.menu.pack_propagate(False)

        # Logo / nome
        logo = tk.Label(
            self.menu,
            text="PROAGRO",
            font=("Arial", 22, "bold"),
            fg="white",
            bg="#173F2A"
        )

        logo.pack(
            pady=(35, 5)
        )

        subtitulo = tk.Label(
            self.menu,
            text="CONSULTORIA",
            font=("Arial", 9),
            fg="#B7D8C4",
            bg="#173F2A"
        )

        subtitulo.pack(
            pady=(0, 35)
        )

        # Botões
        botoes = [
            ("⌂   Início", self.inicio),
            ("♙   Clientes", self.clientes),
            ("⌖   Propriedades", self.propriedades),
            ("▣   Serviços", self.servicos),
            ("▤   Equipamentos", self.equipamentos),
            ("$   Financeiro", self.financeiro),
            ("▧   Documentos", self.documentos),
            ("▥   Relatórios", self.relatorios),
        ]

        for texto, comando in botoes:

            botao = tk.Button(
                self.menu,
                text=texto,
                command=comando,
                anchor="w",
                font=("Arial", 11),
                fg="white",
                bg="#173F2A",
                activebackground="#245C3E",
                activeforeground="white",
                relief="flat",
                bd=0,
                padx=25,
                pady=12,
                cursor="hand2"
            )

            botao.pack(
                fill="x"
            )

        # ==============================
        # ÁREA PRINCIPAL
        # ==============================

        self.conteudo = tk.Frame(
            self.root,
            bg="#F4F7F5"
        )

        self.conteudo.pack(
            side="right",
            fill="both",
            expand=True
        )

        self.inicio()

    # ==================================
    # PÁGINAS
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
            fg="#173F2A",
            bg="#F4F7F5"
        )

        titulo.pack(
            anchor="w",
            padx=40,
            pady=(35, 5)
        )

        subtitulo = tk.Label(
            self.conteudo,
            text="Visão geral do sistema",
            font=("Arial", 11),
            fg="#66756D",
            bg="#F4F7F5"
        )

        subtitulo.pack(
            anchor="w",
            padx=40
        )

        # Cards
        cards = tk.Frame(
            self.conteudo,
            bg="#F4F7F5"
        )

        cards.pack(
            fill="x",
            padx=40,
            pady=35
        )

        self.criar_card(
            cards,
            "CLIENTES",
            "0",
            0
        )

        self.criar_card(
            cards,
            "SERVIÇOS",
            "0",
            1
        )

        self.criar_card(
            cards,
            "EQUIPAMENTOS",
            "0",
            2
        )

        self.criar_card(
            cards,
            "DOCUMENTOS",
            "0",
            3
        )

    def criar_card(
        self,
        parent,
        titulo,
        valor,
        coluna
    ):

        card = tk.Frame(
            parent,
            bg="white",
            width=190,
            height=120,
            highlightbackground="#D8E2DC",
            highlightthickness=1
        )

        card.grid(
            row=0,
            column=coluna,
            padx=8,
            sticky="nsew"
        )

        parent.grid_columnconfigure(
            coluna,
            weight=1
        )

        tk.Label(
            card,
            text=titulo,
            font=("Arial", 9, "bold"),
            fg="#718078",
            bg="white"
        ).pack(
            anchor="w",
            padx=18,
            pady=(18, 5)
        )

        tk.Label(
            card,
            text=valor,
            font=("Arial", 26, "bold"),
            fg="#173F2A",
            bg="white"
        ).pack(
            anchor="w",
            padx=18
        )

    # ==================================
    # MÓDULOS
    # ==================================

    def clientes(self):
        self.limpar_conteudo()
        # Importa e instancia a tela real de clientes
        from interface.clientes import TelaClientes
        TelaClientes(self.conteudo, self)

    def propriedades(self):
        self.mostrar_pagina("Propriedades")

    def servicos(self):
        self.mostrar_pagina("Serviços")

    def equipamentos(self):
        self.mostrar_pagina("Equipamentos")

    def financeiro(self):
        self.mostrar_pagina("Financeiro")

    def documentos(self):
        self.mostrar_pagina("Documentos")

    def relatorios(self):
        self.mostrar_pagina("Relatórios")

    def mostrar_pagina(self, nome):

        self.limpar_conteudo()

        tk.Label(
            self.conteudo,
            text=nome,
            font=("Arial", 26, "bold"),
            fg="#173F2A",
            bg="#F4F7F5"
        ).pack(
            anchor="w",
            padx=40,
            pady=(35, 5)
        )

        tk.Label(
            self.conteudo,
            text="Módulo em desenvolvimento",
            font=("Arial", 11),
            fg="#66756D",
            bg="#F4F7F5"
        ).pack(
            anchor="w",
            padx=40
        )