"""Módulo de execução de processos Web via Selenium"""

import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

logger = logging.getLogger(__name__)


def driver_init():
    """Inicializa o WebDriver."""

    driver = webdriver.Chrome()
    wait = WebDriverWait(driver, 10)
    return driver, wait


def gerar_pessoa(driver, wait):
    """Configura Brasil e gera uma identidade fictícia."""

    logger.info("Acessando Fake Name Generator.")
    driver.get("https://www.fakenamegenerator.com/")

    logger.info("Configurando o site para geração do comprador.")
    nome = Select(
        wait.until(
            EC.presence_of_element_located((By.ID, "n"))
        )
    )
    nome.select_by_value("br")

    pais = Select(
        wait.until(
            EC.presence_of_element_located((By.ID, "c"))
        )
    )
    pais.select_by_value("br")

    logger.info("Gerando comprador.")

    driver.find_element(By.ID, "genbtn").click()

    wait.until(
        EC.visibility_of_element_located(
            (By.CSS_SELECTOR, ".address h3")
        )
    )

    logger.info("Comprador gerado com sucesso.")


def capturar_dados(wait):
    """Captura nome, sobrenome e CEP da identidade gerada."""

    nome = wait.until(
        EC.visibility_of_element_located(
            (By.CSS_SELECTOR, ".address h3")
        )
    )

    endereco = wait.until(
        EC.visibility_of_element_located(
            (By.CSS_SELECTOR, ".address .adr")
        )
    )

    nome_completo = nome.text.strip()
    endereco = endereco.text.strip()

    nome_fracionado = nome_completo.split()
    endereco_fracionado = endereco.splitlines()

    if len(nome_fracionado) < 2:
        raise ValueError(
            f"Nome retornado em formato inesperado: {nome_completo!r}"
        )

    if not endereco_fracionado:
        raise ValueError(
            f"Endereço retornado em formato inesperado: {endereco!r}"
        )

    comprador = {
        "Nome": nome_fracionado[0],
        "Sobrenome": " ".join(nome_fracionado[1:]),
        "CEP": endereco_fracionado[-1].strip(),
    }

    logger.info(
        "Dados do comprador capturados com sucesso."
    )

    return comprador


def acessar_sauce(driver, wait):
    """Acessa o Sauce Demo e realiza o login."""
    logger.info("Acessando Sauce Demo.")
    driver.get("https://www.saucedemo.com/")

    usuario = wait.until(
        EC.visibility_of_element_located((By.ID, "user-name"))
    )
    senha = driver.find_element(By.ID, "password")

    usuario.send_keys("standard_user")
    senha.send_keys("secret_sauce")

    driver.find_element(By.ID, "login-button").click()

    wait.until(
        EC.visibility_of_element_located(
            (By.CLASS_NAME, "inventory_list")
        )
    )

    logger.info("Login no Sauce Demo realizado com sucesso.")


def capturar_produtos(wait):
    """Captura o catálogo completo de produtos do Sauce Demo."""
    logger.info("Iniciando captura do catálogo.")

    itens_inventario = wait.until(
        EC.presence_of_all_elements_located(
            (By.CLASS_NAME, "inventory_item")
        )
    )

    produtos = []

    for item in itens_inventario:
        link = item.find_element(
            By.CSS_SELECTOR,
            "a[id$='_title_link']"
        )

        id_link = link.get_attribute("id")
        partes_id = id_link.split("_")
        if len(partes_id) < 2 or not partes_id[1].isdigit():
            raise ValueError(
                f"ID de produto em formato inesperado: {id_link!r}"
            )
        numero = partes_id[1]

        nome = item.find_element(
            By.CLASS_NAME,
            "inventory_item_name"
        ).text.strip()

        descricao = item.find_element(
            By.CLASS_NAME,
            "inventory_item_desc"
        ).text.strip()

        preco = item.find_element(
            By.CLASS_NAME,
            "inventory_item_price"
        ).text.strip()

        produto = {
            "Numero": numero,
            "Nome": nome,
            "Descricao": descricao,
            "Preco": preco
        }

        produtos.append(produto)

        logger.info(
            "Produto coletado | Nº %s | %s | %s",
            numero,
            nome,
            preco
        )

    produtos.sort(key=lambda produto: int(produto["Numero"]))

    logger.info(
        "Catálogo coletado com sucesso. Total: %d produtos.",
        len(produtos)
    )

    return produtos
