from pathlib import Path
from openpyxl import load_workbook


ARQUIVO_EXCEL = Path(__file__).parent / "SistemaAgronomia.xlsx"


def abrir_excel():
    if not ARQUIVO_EXCEL.exists():
        raise FileNotFoundError(
            f"Arquivo Excel não encontrado:\n{ARQUIVO_EXCEL}"
        )

    return load_workbook(ARQUIVO_EXCEL)


def encontrar_tabela(wb, nome_tabela):

    for ws in wb.worksheets:

        if nome_tabela in ws.tables:

            tabela = ws.tables[nome_tabela]

            return ws, tabela

    raise ValueError(
        f"A tabela '{nome_tabela}' não foi encontrada."
    )


def ler_tabela(nome_tabela):

    wb = abrir_excel()

    ws, tabela = encontrar_tabela(
        wb,
        nome_tabela
    )

    dados = list(ws[tabela.ref])

    cabecalho = [
        celula.value
        for celula in dados[0]
    ]

    resultado = []

    for linha in dados[1:]:

        valores = [
            celula.value
            for celula in linha
        ]

        if not any(
            valor is not None
            for valor in valores
        ):
            continue

        resultado.append(
            dict(zip(cabecalho, valores))
        )

    return resultado


def gerar_id_cliente():

    clientes = ler_tabela("tbClientes")

    maior_id = 0

    for cliente in clientes:

        id_cliente = cliente.get("ID_CLIENTE")

        if not id_cliente:
            continue

        try:
            numero = int(
                id_cliente.split("-")[1]
            )

            maior_id = max(
                maior_id,
                numero
            )

        except (ValueError, IndexError):
            continue

    proximo = maior_id + 1

    return f"CLI-{proximo:03d}"


def adicionar_cliente(dados):

    wb = abrir_excel()

    ws, tabela = encontrar_tabela(
        wb,
        "tbClientes"
    )

    # Descobre os limites atuais da tabela
    inicio, fim = tabela.ref.split(":")

    # Coluna e linha inicial
    coluna_inicial = ws[inicio].column
    linha_inicial = ws[inicio].row

    # Coluna e linha final
    coluna_final = ws[fim].column
    linha_final = ws[fim].row

    # A próxima linha será logo abaixo da tabela
    proxima_linha = linha_final + 1

    # Obtém os cabeçalhos da tabela
    cabecalho = []

    for coluna in range(
        coluna_inicial,
        coluna_final + 1
    ):
        cabecalho.append(
            ws.cell(
                linha_inicial,
                coluna
            ).value
        )

    # Insere os dados
    for coluna, nome_coluna in enumerate(
        cabecalho,
        start=coluna_inicial
    ):

        valor = dados.get(
            nome_coluna,
            ""
        )

        ws.cell(
            proxima_linha,
            coluna,
            valor
        )

    # Atualiza o intervalo da tabela
    nova_referencia = (
        f"{inicio}:"
        f"{ws.cell(proxima_linha, coluna_final).coordinate}"
    )

    tabela.ref = nova_referencia

    # Salva o Excel
    wb.save(ARQUIVO_EXCEL)

    # Expande a tabela
    inicio = tabela.ref.split(":")[0]
    fim_coluna = ws.cell(
        1,
        coluna_inicial + len(cabecalho) - 1
    ).column_letter

    tabela.ref = (
        f"{inicio}:{fim_coluna}{proxima_linha}"
    )

    wb.save(ARQUIVO_EXCEL)