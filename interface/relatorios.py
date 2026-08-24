import tkinter as tk
from tkinter import ttk
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))
from excel import ler_tabela


class TelaRelatorios:

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

        titulo = tk.Label(topo, text="Relatórios e Resumos", font=("Arial", 26, "bold"), fg="#173F2A", bg="#F4F7F5")
        titulo.pack(side="left")

        # Container de cartões de resumo
        cards_frame = tk.Frame(self.conteudo, bg="#F4F7F5")
        cards_frame.pack(fill="x", padx=40, pady=(0, 20))

        try:
            total_clientes = len(ler_tabela("tbClientes"))
            total_prop = len(ler_tabela("tbPropriedades"))
            total_serv = len(ler_tabela("tbServicos"))
            total_eqp = len(ler_tabela("tbEquipamentos"))
        except:
            total_clientes = total_prop = total_serv = total_eqp = 0

        self.criar_card(cards_frame, "Total Clientes", str(total_clientes), "#245C3E", 0)
        self.criar_card(cards_frame, "Propriedades", str(total_prop), "#2980B9", 1)
        self.criar_card(cards_frame, "Serviços", str(total_serv), "#D35400", 2)
        self.criar_card(cards_frame, "Equipamentos", str(total_eqp), "#8E44AD", 3)

        # Informação descritiva inferior
        info_frame = tk.Frame(self.conteudo, bg="white", relief="solid", bd=1)
        info_frame.pack(fill="both", expand=True, padx=40, pady=(0, 40))

        tk.Label(info_frame, text="Central de Relatórios ProAgro", font=("Arial", 16, "bold"), fg="#173F2A", bg="white").pack(anchor="w", padx=20, pady=20)
        tk.Label(info_frame, text="Todos os dados são extraídos em tempo real diretamente das tabelas do seu arquivo Excel.\nUtilize os módulos laterais para cadastrar novos registros e gerenciar operações.", font=("Arial", 11), fg="#555", bg="white", justify="left").pack(anchor="w", padx=20)

    def criar_card(self, parent, titulo, valor, cor, coluna):
        card = tk.Frame(parent, bg="white", relief="solid", bd=1, padx=20, pady=15)
        card.grid(row=0, column=coluna, sticky="nsew", padx=(0, 15))
        parent.grid_columnconfigure(coluna, weight=1)

        tk.Label(card, text=titulo, font=("Arial", 10, "bold"), fg="#777", bg="white").pack(anchor="w")
        tk.Label(card, text=valor, font=("Arial", 22, "bold"), fg=cor, bg="white").pack(anchor="w", pady=(5, 0))