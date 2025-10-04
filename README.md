Consulta de Ações da B3 com Flask e Selenium
Este é um projeto de web scraping que utiliza Flask como framework web e Selenium para automatizar a coleta de dados de ações do mercado brasileiro (B3) diretamente do portal Yahoo Finance.

A aplicação permite duas funcionalidades principais:

Cotação em Tempo Real: Busca o valor atual, a variação diária e a variação percentual de uma ação específica.

Dados Históricos: Permite ao usuário selecionar um período (data de início e fim) para visualizar o histórico de cotações de uma ação, incluindo valores de abertura, máxima, mínima, fechamento e volume negociado.

Tecnologias Utilizadas
Python: Linguagem de programação principal.

Flask: Micro-framework web para criar a interface e a API.

Selenium: Ferramenta de automação de navegadores para realizar o web scraping.

HTML, CSS (TailwindCSS) e JavaScript: Para a construção da interface do usuário (frontend).

Pré-requisitos
Antes de começar, você precisará ter o seguinte instalado em sua máquina:

Python 3.8+

O navegador Google Chrome.

Guia de Instalação e Execução
Siga os passos abaixo para configurar e rodar o projeto em seu ambiente local.

1. Clone o Repositório
Se você baixou como .zip, apenas descompacte o projeto em uma pasta de sua preferência.

2. Crie um Ambiente Virtual (Virtual Environment)
É uma boa prática criar um ambiente virtual para isolar as dependências do projeto. Abra o terminal na pasta raiz do projeto e execute:

# Cria o ambiente virtual
python -m venv venv

# Ativa o ambiente virtual
# No Windows:
venv\Scripts\activate
# No macOS/Linux:
source venv/bin/activate

3. Instale as Dependências
Com o ambiente virtual ativado, instale todas as bibliotecas necessárias usando o arquivo requirements.txt.

pip install -r requirements.txt

4. Baixe o ChromeDriver
Esta aplicação utiliza o chromedriver para que o Selenium possa controlar o Google Chrome.

Verifique a Versão do seu Chrome: Abra o Chrome, vá para Menu (três pontos) > Ajuda > Sobre o Google Chrome e anote a sua versão (ex: 120.0.6099.110).

Baixe o Driver Correto:

Acesse o painel oficial: Chrome for Testing availability

Encontre a seção da sua versão (use os primeiros números, ex: 120.0.6099).

Na coluna chromedriver, clique no link de download para win64.

Posicione o Arquivo:

Descompacte o arquivo baixado.

Copie o arquivo chromedriver.exe e cole-o na pasta raiz do seu projeto, ao lado do arquivo app.py.

5. Execute a Aplicação
Com tudo configurado, execute o servidor Flask com o seguinte comando:

python app.py

Você verá uma mensagem indicando que o servidor está rodando, algo como:
* Running on http://127.0.0.1:5000

Como Usar
Abra seu navegador web e acesse o endereço: http://127.0.0.1:5000

Para Cotação em Tempo Real:

Digite o código da ação (ex: PETR4, MGLU3, ITUB4) no campo "Código da Ação".

Deixe os campos de data em branco.

Clique no botão "Buscar".

Para Dados Históricos:

Digite o código da ação.

Selecione uma "Data de Início" e uma "Data de Fim" nos calendários.

Clique no botão "Buscar".

A aplicação exibirá os resultados abaixo do formulário de busca.