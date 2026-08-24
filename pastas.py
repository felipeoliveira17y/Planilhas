from pathlib import Path
import re


PASTA_CLIENTES = Path(__file__).parent / "Cliente"


def limpar_nome(nome):
    """
    Remove caracteres que não podem ser usados
    em nomes de arquivos e pastas no Windows.
    """

    caracteres_invalidos = r'[<>:"/\\|?*]'

    nome = re.sub(
        caracteres_invalidos,
        "",
        nome
    )

    return nome.strip()


def criar_pasta_cliente(id_cliente, nome_cliente):

    nome_cliente = limpar_nome(nome_cliente)

    pasta_cliente = (
        PASTA_CLIENTES /
        f"{id_cliente} - {nome_cliente}"
    )

    subpastas = [
        "Documentação",
        "Serviços",
        "Financeiro",
        "Outros"
    ]

    # Cria a pasta principal
    pasta_cliente.mkdir(
        parents=True,
        exist_ok=True
    )

    # Cria as subpastas
    for subpasta in subpastas:

        (pasta_cliente / subpasta).mkdir(
            exist_ok=True
        )

    return pasta_cliente