import requests
import time

def scraper(pesquisado="", ordem="relevancia"):
    url = "https://qknhp8tc3y-dsn.algolia.net/1/indexes/produits_pt/query?x-algolia-agent=Algolia%20for%20vanilla%20JavaScript%20(lite)%203.24.7&x-algolia-application-id=QKNHP8TC3Y&x-algolia-api-key=93946b91c013211f842ddf1819ea880b"
    
    cabecalhos = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36",
        "Origin": "https://www.instant-gaming.com",
        "Referer": "https://www.instant-gaming.com/",
        "Accept": "application/json",
        "Content-Type":"application/x-www-form-urlencoded"
    }

    jogos_extraidos = []

    for numero_pagina in range(0,3):
        dados_envio = '{"params":"query='+ pesquisado +'&hitsPerPage=60&filters=(platforms%3A4)%20AND%20(is_prepaid%3A0)%20AND%20(is_subscription%3A0)%20AND%20(country_whitelist%3APT%20OR%20country_whitelist%3Aworldwide%20OR%20country_whitelist%3AWW)%20AND%20(NOT%20country_blacklist%3APT)%20AND%20is_draft%3A0&facets=%5B%22search_tags%22%2C%22langs_audio%22%2C%22langs_subtitle%22%5D&maxValuesPerFacet=1000&page='+str(numero_pagina)+ '"}'
        try: 
            resposta = requests.post(url, headers=cabecalhos, data=dados_envio)
            if resposta.status_code == 200:
                json_resposta = resposta.json()
                lista_jogos = json_resposta.get("hits", [])

                for jogo in lista_jogos:
                    id_jogo = jogo.get("prod_id", "")
                    nome_seo = jogo.get("seo_name", "")
                    link_img = f"https://gaming-cdn.com/images/products/{id_jogo}/271x377/{nome_seo}-cover.jpg"
                    pacote_jogo = {
                        "nome": jogo.get("name", "Nome desconhecido"),
                        "preco": jogo.get("price_eur", "0.00"),
                        "desconto": jogo.get("discount", 0),
                        "imagem": link_img
                    }
                    jogos_extraidos.append(pacote_jogo)
        
            
        except Exception as erro:
            print(f"Erro na ligação: {erro}")

        time.sleep(1)
    if ordem == "preco_asc":
        jogos_extraidos.sort(key=lambda x: float(x["preco"]))
    elif ordem == "preco_desc":
        jogos_extraidos.sort(key=lambda x: float(x["preco"]), reverse=True)
    elif ordem == "desconto":
        jogos_extraidos.sort(key=lambda x: x["desconto"], reverse=True)

    return jogos_extraidos

if __name__ == "__main__":
    scraper()