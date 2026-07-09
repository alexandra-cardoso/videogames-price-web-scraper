# Comparador de Preços de Videojogos (Web Scraper)
Projeto Full-Stack em Python que extrai e permite ao utilizador comparar preços para o mesmo videojogo em sites como a Instant Gaming e a Nintendo eShop.

## Tecnologias Utilizadas
* **Backend:** Python, Flask, Requests
* **Processamento:** Manipulação de APIs (Engenharia Reversa) e ficheiros JSON
* **Frontend:** HTML5, CSS3, Jinja2

## Como funciona
O projeto está dividido numa arquitetura desacoplada:
1. Um robô (`run_scraper.py`) que extrai os dados em background e constrói um ficheiro (`jogos.json`) como base de dados local em que guarda todos os dados necessários para identificar o jogo e verificar o preço e desconto aplicado, ou não.
2. Uma aplicação web (`app.py`) que serve os dados instantaneamente, graças à base de dados definida no ficheiro json criada anteriormente, para o utilizador.

## Como Instalar e Correr o Projeto
### 1. Pré-Requisitos
Certifica-te de que tem o [Python](https://www.python.org/) instalado no seu computador.
### 2. Clonar o Repositório
No terminal, clone o projeto para a sua máquina:
git clone [https://github.com/alexandra-cardoso/videogames-price-web-scraper.git](https://github.com/alexandra-cardoso/videogames-price-web-scraper.git)
cd videogames-price-web-scraper
### 3. Criar e Ativar o Ambiente Virtual
Para não misturar bibliotecas utilizadas neste projeto com as presentes no seu computador, criamos um ambiente virtual:
*No Windows:*
python -m venv venv
venv\Scripts\activate
*No Max/Linux:*
python3 -m venv venv
source venv/bin/activate
### 4. Instalar as Dependências
Instalar as bibliotecas identificadas no ficheiro de requisitos (`requirements.txt`):
pip install -r requirements.txt
### 5. Gerar a Base de Dados (Fase 1)
É possível gerar a base de dados correndo o ficheiro `run_scraper.py` com o comando:
python run_scraper.py
*(Nota: o processo pode/deve demorar algum tempo, dependendo de quantos jogos quiser na sua base de dados. Além disso, são feitas pausas pontuais na procura para evitar bloqueios por parte dos servidores dos websites)*
### 6. Ligar o Servidor Web (Fase 2)
Ao obter o ficheiro JSON, ligar a aplicação Flask é simples, com o comando:
python app.py
Abrindo o navegador e acedendo a http://127.0.0.1:5000/ é possível verificar o resultado da pesquisa.