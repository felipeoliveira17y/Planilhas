import ctypes
import os
import tkinter as tk
from interface.dashboard import Dashboard


def main():
    # Força o Windows a separar o app do processo padrão do Python na barra de tarefas
    try:
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(
            "landmensure.sistema.gestao.1.0"
        )
    except:
        pass

    root = tk.Tk()
    root.title("Landmensure")

    nome_arquivo_icone = "icone.ico"

    if os.path.exists(nome_arquivo_icone):
        try:
            root.iconbitmap(nome_arquivo_icone)
        except Exception as e:
            print("Erro ao carregar o ícone:", e)
    else:
        print(f"O arquivo '{nome_arquivo_icone}' não foi encontrado na raiz do projeto.")

    app = Dashboard(root)
    root.mainloop()


if __name__ == "__main__":
    main()