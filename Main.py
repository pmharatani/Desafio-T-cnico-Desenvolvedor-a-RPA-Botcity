"""Módulo principal - orquestra a execução da automação"""

import logging

from Config import (
    configurar_logger,
    preparar_diretorios,
    SCREENSHOTS_DIR,
    RESULTS_DIR)
from Ferramentas import (
    salvar_comprador_csv,
    salvar_catalogo_csv,
    ler_csv)
from Web import (
    driver_init,
    gerar_pessoa,
    capturar_dados,
    acessar_sauce,
    capturar_produtos)
from Fakturama import FakturamaBot


def main():
    preparar_diretorios()
    configurar_logger()
    logger = logging.getLogger(__name__)

    logger.info("Iniciando automação.")

    driver = None
    bot = None

    try:
        logger.info("Iniciando etapa Web.")
        driver, wait = driver_init()

        gerar_pessoa(driver, wait)
        comprador = capturar_dados(wait)

        logger.info(
            "Comprador gerado | Nome: %s %s | CEP: %s",
            comprador["Nome"],
            comprador["Sobrenome"],
            comprador["CEP"]
        )

        # Captura de tela para evidência de clientes
        driver.save_screenshot(
            str(SCREENSHOTS_DIR / "Comprador_FNG.png")
        )
        logger.info("Screenshot do comprador no Fake Name Generator capturado.")

        salvar_comprador_csv(comprador)

        acessar_sauce(driver, wait)

        produtos = capturar_produtos(wait)

        # Captura de tela para evidência de produtos
        driver.save_screenshot(
            str(SCREENSHOTS_DIR / "Produtos_Sauce.png")
        )
        logger.info("Screenshot do catálogo no Sauce Demo capturado.")

        # Salva os dados dos produtos em CSV para uso posterior
        salvar_catalogo_csv(produtos)

        driver.quit()
        driver = None

        logger.info("Etapa Web finalizada.")

        # Leitura dos CSVs previamente gerados como ponte entre as etapas de execução
        compradores_csv = ler_csv(RESULTS_DIR / "Comprador.csv")
        produtos_csv = ler_csv(RESULTS_DIR / "Catalogo.csv")

        logger.info("Iniciando etapa Fakturama.")
        bot = FakturamaBot()
        bot.iniciar_fakturama()

        # Iteração pelos clientes presentes no CSV, cadastrando-os no Fakturama
        logger.info("Iniciando registro dos compradores.")
        for comprador in compradores_csv:
            logger.info("Cadastrando comprador %s %s.",
                        comprador["Nome"],
                        comprador["Sobrenome"])
            bot.abrir_aba("Novo contato", "novo_contato", "label_nomes")
            bot.preencher_comprador(comprador)
            bot.salvar()
            bot.fechar_aba()
            logger.info("Comprador cadastrado com sucesso.")
        logger.info("Registro dos compradores finalizado.")

        # Iteração pelos produtos presentes no CSV, cadastrando-os no Fakturama
        logger.info("Iniciando registro dos produtos.")
        for produto in produtos_csv:
            logger.info(
                "Cadastrando produto | Nº %s | %s",
                produto["Numero"],
                produto["Nome"]
            )
            bot.abrir_aba("Novo produto", "novo_produto", "numero_item")
            bot.preencher_produto(produto)
            bot.salvar()
            bot.fechar_aba()
            logger.info("Produto cadastrado com sucesso.")
        logger.info("Registro dos produtos finalizado.")

        # Abertura do registro de clientes no Fakturama para captura de tela
        logger.info("Realizando captura da tela de Contatos.")
        bot.abrir_aba("Contatos", "contatos", "first_name")
        bot.capturar_screenshot("Contatos_Fakturama")
        bot.fechar_aba()

        # Abertura do registro de produtos no Fakturama para captura de tela
        logger.info("Realizando captura da tela de Produtos.")
        bot.abrir_aba("Produtos", "produtos", "item_no")
        bot.capturar_screenshot("Produtos_Fakturama")
        bot.fechar_aba()

        bot.fechar_fakturama()
        bot = None
        logger.info("Etapa Fakturama finalizada.")

        logger.info("Automação finalizada com sucesso.")

    except Exception:
        logger.exception("Automação finalizada com erro.")
        raise

    finally:
        if driver is not None:
            try:
                driver.quit()
            except Exception:
                logger.exception("Erro ao encerrar o navegador.")
        if bot is not None:
            try:
                bot.fechar_fakturama()
            except Exception:
                logger.exception("Erro ao encerrar o Fakturama.")

if __name__ == "__main__":
    main()
