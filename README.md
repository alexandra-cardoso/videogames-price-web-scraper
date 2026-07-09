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