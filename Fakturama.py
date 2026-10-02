"""Módulo de interação com o sistema Fakturama."""

import logging
import os
from pathlib import Path
from botcity.core import Backend, DesktopBot
from pywinauto.timings import wait_until_passes
from Config import ASSETS_DIR, SCREENSHOTS_DIR

logger = logging.getLogger(__name__)


class FakturamaBot(DesktopBot):
    """Classe responsável pelas operações no Fakturama."""

    def __init__(self):
        super().__init__()

        imagens = [
            "label_nomes",
            "novo_contato",
            "novo_produto",
            "numero_item",
            "contatos",
            "produtos",
            "item_no",
            "first_name"
        ]

        for imagem in imagens:
            caminho = ASSETS_DIR / f"{imagem}.png"
            if not caminho.is_file():
                raise FileNotFoundError(
                    f"Asset obrigatório não encontrado: {caminho}"
                )
            self.add_image(imagem, str(caminho))

    def encontrar(self, nome, matching=0.90, timeout=10000):
        """Procura um elemento visual na tela."""

        if not self.find(
            nome,
            matching=matching,
            waiting_time=timeout
        ):
            raise RuntimeError(f"Elemento '{nome}' não encontrado.")

        elemento = self.get_last_element()

        return elemento

    def localizar_atalho_fakturama(self):
        """Procura o atalho do Fakturama nos locais padrão do Windows."""

        diretorios = [
            Path(os.environ["APPDATA"])
            / "Microsoft/Windows/Start Menu/Programs",

            Path(os.environ["PROGRAMDATA"])
            / "Microsoft/Windows/Start Menu/Programs",

            Path.home() / "Desktop"
        ]

        for diretorio in diretorios:
            if not diretorio.exists():
                continue

            for arquivo in diretorio.rglob("*.lnk"):
                if "fakturama" in arquivo.stem.lower():
                    return arquivo

        return None

    def aguardar_processo_fakturama(self, timeout=30):
        """Aguarda o processo do Fakturama ficar disponível."""

        def encontrar_processo():
            processo = self.find_process(name="Fakturama")

            if processo is None:
                raise RuntimeError(
                    "Processo do Fakturama ainda não disponível."
                )

            return processo

        try:
            return wait_until_passes(
                timeout=timeout,
                retry_interval=0.5,
                func=encontrar_processo
            )

        except Exception as erro:
            raise RuntimeError(
                f"Fakturama não iniciou em até {timeout} segundos."
            ) from erro

    def conectar_fakturama(self, processo):
        """Conecta à janela principal do Fakturama."""

        logger.info("Conectando ao Fakturama | PID: %s", processo.pid)

        self.connect_to_app(
            Backend.WIN_32,
            process=processo.pid
        )

        self.find_app_window(
            title_re=r"^Fakturama - .+",
            class_name="SWT_Window0",
            waiting_time=60000
        )

        logger.info("Janela principal do Fakturama localizada.")

    def iniciar_fakturama(self):
        """
        Localiza uma instância existente do Fakturama ou inicia
        a aplicação através de um atalho do Windows.
        """

        logger.info("Inicializando Fakturama.")

        processo = self.find_process(name="Fakturama")

        if processo is None:
            logger.info("Fakturama não está em execução. Procurando atalho.")

            atalho = self.localizar_atalho_fakturama()

            if atalho is None:
                raise RuntimeError(
                    "Atalho do Fakturama não encontrado."
                )

            logger.info("Abrindo Fakturama através de: %s", atalho)

            self.execute(str(atalho))

            processo = self.aguardar_processo_fakturama()

        else:
            logger.info("Fakturama já está em execução | PID: %s", processo.pid)

        self.conectar_fakturama(processo)

        # Só considera o Fakturama carregado quando um
        # elemento da interface final estiver disponível.
        self.encontrar(
            "novo_contato",
            timeout=60000
        )

        logger.info("Fakturama carregado. Maximizando janela.")

        self.maximize_window()

        logger.info("Fakturama pronto para automação.")

    def abrir_aba(self, nome_aba, nome_asset, campo_confirmacao):
        """Abre uma aba do Fakturama e confirma seu carregamento."""

        self.encontrar(nome_asset)
        self.click()

        # Confirma que a aba realmente abriu.
        self.encontrar(
            campo_confirmacao,
            matching=0.80
        )

        logger.info("Aba %s aberta.", nome_aba)

    def preencher_comprador(self, comprador):
        """Preenche os dados do comprador no formulário."""

        logger.info(
            "Iniciando preenchimento do comprador: %s %s",
            comprador["Nome"],
            comprador["Sobrenome"]
        )

        elemento = self.encontrar(
            "label_nomes",
            matching=0.80
        )

        # Foco no campo First Name, relativo à âncora visual.
        x = int(elemento.left + 180)
        y = int(elemento.top + elemento.height - 8)

        self.click_at(x, y)

        self.kb_type(
            comprador["Nome"],
            interval=5
        )

        self.tab()

        self.kb_type(
            comprador["Sobrenome"],
            interval=5
        )

        self.tab(presses=8)

        self.kb_type(
            comprador["CEP"],
            interval=5
        )

        logger.info("Comprador preenchido com sucesso.")

    def preencher_produto(self, produto):
        """Preenche os dados do produto no formulário."""

        elemento = self.encontrar(
            "numero_item",
            matching=0.80
        )

        # Posiciona o cursor no campo Item No. em relação à âncora visual.
        x = int(elemento.left + 180)
        y = int(elemento.top + elemento.height - 8)

        self.click_at(x, y)

        self.kb_type(
            produto["Numero"],
            interval=5
        )

        self.tab()

        self.kb_type(
            produto["Nome"],
            interval=5
        )

        self.tab(presses=4)

        self.kb_type(
            produto["Descricao"],
            interval=5
        )

        self.tab()
        preco = produto["Preco"].replace("$", "").replace(".", ",")
        self.kb_type(
            preco,
            interval=5
        )

    def salvar(self):
        """Salva o registro atual no Fakturama."""

        self.control_s()
        logger.info("Comando de salvamento executado.")

    def fechar_aba(self):
        """Fecha a aba atual do Fakturama."""
        self.control_w()

    def fechar_fakturama(self):
        """Encerra o processo do Fakturama."""

        processo = self.find_process(name="Fakturama")

        if processo is None:
            logger.info("Fakturama já está encerrado.")
            return

        logger.info("Encerrando Fakturama | PID: %s", processo.pid)

        self.terminate_process(processo)

        logger.info("Fakturama encerrado com sucesso.")

    def capturar_screenshot(self, nome):
        """Captura a tela atual e salva na pasta de evidências."""

        caminho = SCREENSHOTS_DIR / f"{nome}.png"

        self.save_screenshot(str(caminho))

        logger.info("Screenshot capturado com sucesso: %s", caminho)
