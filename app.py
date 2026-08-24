import ctypes
import os
import tkinter as tk
from interface.dashboard import Dashboard


def main():
    # 1. Define o ID exclusivo para o Windows ANTES de criar qualquer janela
    try:
        myappid = "landmensure.sistema.gestao.1.0"
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
    except Exception as e:
        print("Erro ao definir AppUserModelID:", e)

    root = tk.Tk()
    root.title("Landmensure - Sistema de Gestão")

    # 2. Caminho para os ícones dentro da pasta "img"
    caminho_icone_principal = os.path.join("img", "icone2.ico")
    caminho_icone_alternativo = os.path.join("img", "icone.ico")

    if os.path.exists(caminho_icone_principal):
        try:
            root.iconbitmap(caminho_icone_principal)
        except Exception as e:
            print("Erro ao carregar o ícone principal:", e)
    elif os.path.exists(caminho_icone_alternativo):
        try:
            root.iconbitmap(caminho_icone_alternativo)
        except Exception as e:
            print("Erro ao carregar o ícone alternativo:", e)
    else:
        print("Nenhum arquivo de ícone foi encontrado na pasta 'img'.")

    app = Dashboard(root)
    root.mainloop()


if __name__ == "__main__":
    main()