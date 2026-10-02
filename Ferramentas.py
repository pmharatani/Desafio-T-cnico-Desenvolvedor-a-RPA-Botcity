"""Módulo Auxiliar - Funções auxiliares do projeto."""
import csv
import logging
from Config import RESULTS_DIR

logger = logging.getLogger(__name__)


def salvar_comprador_csv(comprador):
    """Salva os dados do comprador em arquivo CSV."""
    caminho = RESULTS_DIR / "Comprador.csv"
    campos = ["Nome", "Sobrenome", "CEP"]

    for campo in campos:
        if not comprador.get(campo):
            raise ValueError(
                f"Campo obrigatório ausente no comprador: {campo}"
            )

    with open(
        caminho,
        mode="w",
        newline="",
        encoding="utf-8-sig"
    ) as arquivo:

        writer = csv.DictWriter(
            arquivo,
            fieldnames=campos
        )

        writer.writeheader()
        writer.writerow(comprador)

    logger.info(
        "CSV do comprador salvo com sucesso: %s",
        caminho
    )

    return caminho


def salvar_catalogo_csv(produtos):
    """Salva os dados do catálogo em arquivo CSV."""

    caminho = RESULTS_DIR / "Catalogo.csv"

    campos = ["Numero", "Nome", "Descricao", "Preco"]

    if not produtos:
        raise ValueError("O catálogo não possui produtos.")

    for produto in produtos:
        numero = produto.get("Numero", "desconhecido")
        for campo in campos:
            if not produto.get(campo):
                raise ValueError(
                    f"Campo obrigatório ausente no produto "
                    f"{numero}: {campo}"
                )

    with open(
        caminho,
        mode="w",
        newline="",
        encoding="utf-8-sig"
    ) as arquivo:

        writer = csv.DictWriter(
            arquivo,
            fieldnames=campos
        )

        writer.writeheader()
        writer.writerows(produtos)

    logger.info(
        "CSV do catálogo salvo com sucesso | %d produtos | %s",
        len(produtos),
        caminho
    )

    return caminho


def ler_csv(caminho):
    """Lê um arquivo CSV e retorna seus registros como dicionários."""
    with open(
        caminho,
        "r",
        newline="",
        encoding="utf-8-sig"
    ) as arquivo:
        reader = csv.DictReader(arquivo)
        valores = list(reader)

    if not valores:
        raise RuntimeError(
            f"O CSV '{caminho}' está vazio."
        )

    logger.info(
        "CSV carregado com sucesso: %s",
        caminho
    )

    return valores
