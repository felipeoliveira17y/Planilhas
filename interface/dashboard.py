import os
import customtkinter as ctk
from PIL import Image
from excel import ler_tabela

# Configuração global de tema do CustomTkinter
ctk.set_appearance_mode("System")  # Segue o tema do Windows (Dark/Light)
ctk.set_default_color_theme("dark-blue")


class Dashboard:

    def __init__(self, root):
        self.root = root
        self.root.title("Landmensure - Sistema de Gestão")
        self.root.geometry("1200x700")
        self.root.minsize(1000, 600)

        # Paleta de Cores Moderna (Laranja e Preto Elegante)
        self.cor_menu = "#161616"
        self.cor_laranja = "#FF6600"
        self.cor_hover = "#2A2A2A"
        self.cor_conteudo = "#F4F7F5"

        # Estado da bandeja (False = recolhida, True = expandida)
        self.menu_expandido = False

        self.criar_interface()

    def criar_interface(self):
        # ==============================
        # MENU LATERAL (BANDEJA ESTILIZADA)
        # ==============================
        self.menu = ctk.CTkFrame(
            self.root,
            fg_color=self.cor_menu,
            corner_radius=0,
            width=70
        )
        self.menu.pack(side="left", fill="y")
        self.menu.pack_propagate(False)

        # Topo do Menu: Botão Animado de Expandir/Recolher
        topo_menu = ctk.CTkFrame(self.menu, fg_color=self.cor_menu, height=60)
        topo_menu.pack(fill="x", pady=10)

        self.btn_toggle = ctk.CTkButton(
            topo_menu,
            text="≡",
            command=self.alternar_menu,
            font=("Arial", 18, "bold"),
            text_color="white",
            fg_color=self.cor_menu,
            hover_color=self.cor_hover,
            corner_radius=8,
            width=40,
            height=40
        )
        self.btn_toggle.pack(side="left", padx=15)

        # Container dos Botões
        self.botoes_container = ctk.CTkScrollableFrame(
            self.menu,
            fg_color=self.cor_menu,
            scrollbar_button_color=self.cor_laranja
        )
        self.botoes_container.pack(fill="both", expand=True, pady=5)

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
        self.conteudo = ctk.CTkFrame(
            self.root,
            fg_color=self.cor_conteudo,
            corner_radius=0
        )
        self.conteudo.pack(side="right", fill="both", expand=True)

        self.inicio()

    def criar_botao_lateral(self, arquivo_icone, texto, comando):
        # Frame individual para o botão unificado
        btn_frame = ctk.CTkFrame(
            self.botoes_container,
            fg_color=self.cor_menu,
            corner_radius=8,
            height=45
        )
        btn_frame.pack(fill="x", pady=6, padx=8)
        btn_frame.pack_propagate(False)

        caminho_img = os.path.join("icons", arquivo_icone)
        imagem_ctk = None
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
                
                imagem_ctk = ctk.CTkImage(light_image=img, dark_image=img, size=(20, 20))
            except Exception as e:
                print(f"Erro ao processar ícone {arquivo_icone}: {e}")

        # Botão ajustado com alinhamento à esquerda perfeito para modo recolhido e expandido
        btn_acao = ctk.CTkButton(
            btn_frame,
            text=f"    {texto}" if self.menu_expandido else "",
            image=imagem_ctk,
            compound="left",
            anchor="w",
            command=comando,
            font=("Arial", 12),
            text_color="#CCCCCC",
            fg_color=self.cor_menu,
            hover_color=self.cor_hover,
            corner_radius=8
        )
        # Margem à esquerda ajustada para centralizar o ícone quando a bandeja estiver recolhida (70px)
        btn_acao.pack(fill="both", expand=True, padx=8, pady=2)

        # Guardamos referências para manipulação na expansão
        btn_frame.btn_acao = btn_acao
        btn_frame.texto_original = texto
        btn_frame.icone = imagem_ctk

        return btn_frame

    def alternar_menu(self):
        """Expande ou recolhe a bandeja lateral com fluidez"""
        if self.menu_expandido:
            # Recolher
            self.menu.configure(width=70)
            for frame in self.botoes_criados:
                frame.btn_acao.configure(text="")
            self.menu_expandido = False
        else:
            # Expandir
            self.menu.configure(width=220)
            for frame in self.botoes_criados:
                frame.btn_acao.configure(text=f"    {frame.texto_original}")
            self.menu_expandido = True

    # ==================================
    # PÁGINAS E CARDS
    # ==================================

    def limpar_conteudo(self):
        for widget in self.conteudo.winfo_children():
            widget.destroy()

    def inicio(self):
        self.limpar_conteudo()

        titulo = ctk.CTkLabel(
            self.conteudo,
            text="Dashboard",
            font=("Arial", 26, "bold"),
            text_color="#1A1A1A"
        )
        titulo.pack(anchor="w", padx=40, pady=(35, 5))

        subtituto = ctk.CTkLabel(
            self.conteudo,
            text="Visão geral do sistema Landmensure",
            font=("Arial", 12),
            text_color="#666666"
        )
        subtituto.pack(anchor="w", padx=40)

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

        cards = ctk.CTkFrame(self.conteudo, fg_color="transparent")
        cards.pack(fill="x", padx=40, pady=35)

        self.criar_card(cards, "CLIENTES", total_clientes, 0)
        self.criar_card(cards, "SERVIÇOS", total_servicos, 1)
        self.criar_card(cards, "EQUIPAMENTOS", total_equipamentos, 2)
        self.criar_card(cards, "DOCUMENTOS", total_documentos, 3)
            
    def criar_card(self, parent, titulo, valor, coluna):
        card = ctk.CTkFrame(
            parent,
            fg_color="white",
            corner_radius=10,
            border_width=1,
            border_color="#E0E0E0",
            width=190,
            height=120
        )
        card.grid(row=0, column=coluna, padx=8, sticky="nsew")
        parent.grid_columnconfigure(coluna, weight=1)
        card.pack_propagate(False)

        # Barra laranja fixa no topo do card (usando pack com side="top" para respeitar o espaço)
        barra = ctk.CTkFrame(card, fg_color=self.cor_laranja, height=4, corner_radius=2)
        barra.pack(fill="x", side="top", anchor="n")

        # Container interno para dar respiro aos textos e evitar qualquer sobreposição
        container_textos = ctk.CTkFrame(card, fg_color="transparent")
        container_textos.pack(fill="both", expand=True, padx=18, pady=(10, 10))

        ctk.CTkLabel(
            container_textos,
            text=titulo,
            font=("Arial", 10, "bold"),
            text_color="#777777"
        ).pack(anchor="w", pady=(0, 2))

        ctk.CTkLabel(
            container_textos,
            text=valor,
            font=("Arial", 26, "bold"),
            text_color="#1A1A1A"
        ).pack(anchor="w")

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