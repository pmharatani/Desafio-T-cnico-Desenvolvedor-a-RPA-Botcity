# Desafio Técnico Desenvolvedor(a) RPA - BotCity

Automação desenvolvida em Python 3.11 para o desafio técnico apresentado pela BotCity no processo seletivo para a vaga de Desenvolvedor(a) Python RPA.

## Sobre o Projeto

A automação realiza as seguintes etapas:

- Geração e extração de um comprador fictício no site Fake Name Generator;
- Login e captura do catálogo de produtos do Sauce Demo;
- Registro das informações obtidas em dois arquivos CSV;
- Cadastro do comprador e dos produtos no Fakturama;
- Captura de telas como evidência da execução;
- Geração de logs durante todo o processo;
- Tratamento de erros para facilitar a identificação de possíveis problemas durante a execução.

## Tecnologias Utilizadas

- Python 3.11
- Selenium
- BotCity
- Fakturama

## Pré-requisitos

- Python 3.11;
- Java;
- Fakturama;
- Google Chrome;
- Dependências presentes no `requirements.txt`.

## Instalação

Após clonar o repositório, instale as dependências com:

```bash
pip install -r requirements.txt
```

## Execução

Para iniciar a automação:

```bash
python Main.py
```

A partir daí todo o processo é executado sequencialmente, começando pelas etapas Web e depois seguindo para o Fakturama.

## Estrutura do Projeto

- `Main.py`: fluxo principal da automação;
- `Web.py`: automações do Fake Name Generator e Sauce Demo;
- `Fakturama.py`: automação Desktop do Fakturama;
- `Ferramentas.py`: funções utilizadas para leitura e escrita dos CSVs;
- `Config.py`: configurações de diretórios e logs;
- `assets/`: imagens utilizadas para reconhecimento dos elementos no Fakturama;
- `resultados/`: CSVs, logs e screenshots gerados durante a execução.

## Decisões Técnicas

Para as etapas Web foi utilizado Selenium, já que permite trabalhar diretamente com os elementos das páginas através do DOM.

No Fakturama optei por misturar reconhecimento de imagem com navegação por teclado. Ao invés de depender de coordenadas fixas durante toda a execução, primeiro localizo um elemento da tela por imagem e utilizo ele como referência. A partir desse ponto, a navegação entre os campos é feita principalmente pelo teclado.

Preferi fazer dessa forma porque depender de reconhecimento de imagem para cada campo tornaria a automação mais sensível a pequenas mudanças visuais. Por outro lado, utilizar somente coordenadas fixas também causaria problemas caso a janela estivesse em uma posição diferente.

O BotCity foi utilizado nessa parte da automação porque apresentou bons resultados no reconhecimento das imagens durante os testes e também facilitou a interação com o Fakturama.

## Resultados

Os arquivos gerados pela execução ficam na pasta `resultados/`.

Nela são armazenados:

- `Comprador.csv` com os dados do comprador;
- `Catalogo.csv` com os produtos extraídos do Sauce Demo;
- `execucao.log` com os registros da execução;
- `screenshots/Comprador_FNG.png`;
- `screenshots/Produtos_Sauce.png`;
- `screenshots/Contatos_Fakturama.png`;
- `screenshots/Produtos_Fakturama.png`.

Os screenshots são utilizados como evidência dos dados coletados e dos registros realizados no Fakturama.
