from flask import Flask, render_template, request
import json
import os

app = Flask(__name__)

def load_data():
    if not os.path.exists('jogos.json'):
        return []
    with open('jogos.json', 'r', encoding='utf-8') as f:
        dados=json.load(f)

    jogos_formatados = []
    for slug, info in dados.items():
        precos = [of["preco"] for of in info["ofertas"].values()]
        preco_min = min(precos) if precos else 0.0

        jogos_formatados.append({
            "nome": info["nome"],
            "imagem": info["imagem"],
            "ofertas": info["ofertas"],
            "preco_min": preco_min
        })
    return jogos_formatados

@app.route('/')
def home():
    pesquisado = request.args.get('pesquisa', '').lower()
    filtro = request.args.get('ordem', 'relevancia')
    jogos = load_data()
    jogos_final = []

    for jogo in jogos:
        if pesquisado in jogo["nome"].lower():
            jogos_final.append(jogo)
    
    if filtro == "preco_asc":
        jogos_final.sort(key=lambda x: float(x["preco_min"]))
    elif filtro == "preco_desc":
        jogos_final.sort(key=lambda x: float(x["preco_min"]), reverse=True)
    elif filtro == "desconto":
        jogos_final.sort(key=lambda x: max([of["desconto"] for of in x["ofertas"].values()], default=0), reverse=True)
    
    return render_template('index.html', jogos = jogos_final, pesquisa_atual = request.args.get('pesquisa', ''), ordem_atual=filtro)

if __name__ == '__main__':
    app.run(debug=True)