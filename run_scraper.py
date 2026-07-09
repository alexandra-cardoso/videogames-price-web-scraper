import requests
import json
import time
import re

def gerar_slug(nome):
    nome_limpo=nome.lower()
    nome_limpo=re.sub(r'[^a-z0-9\s-]', '', nome_limpo)
    return re.sub(r'[\s-]+', '-', nome_limpo).strip('-')

def instant(paginas=10):
    url = "https://qknhp8tc3y-dsn.algolia.net/1/indexes/produits_pt/query?x-algolia-agent=Algolia%20for%20vanilla%20JavaScript%20(lite)%203.24.7&x-algolia-application-id=QKNHP8TC3Y&x-algolia-api-key=93946b91c013211f842ddf1819ea880b"
    
    cabecalhos = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36",
        "Origin": "https://www.instant-gaming.com",
        "Referer": "https://www.instant-gaming.com/",
        "Accept": "application/json",
        "Content-Type":"application/x-www-form-urlencoded"
    }
    bd_jogos = {}
    for num_pag in range(0, paginas):
        dados_brutos = '{"params":"query=&hitsPerPage=60&filters=(platforms%3A4)%20AND%20(is_prepaid%3A0)%20AND%20(is_subscription%3A0)%20AND%20(country_whitelist%3APT%20OR%20country_whitelist%3Aworldwide%20OR%20country_whitelist%3AWW)%20AND%20(NOT%20country_blacklist%3APT)%20AND%20is_draft%3A0&facets=%5B%22search_tags%22%2C%22langs_audio%22%2C%22langs_subtitle%22%5D&maxValuesPerFacet=1000&page='+str(num_pag)+ '"}'
        try:
            resposta=requests.post(url, headers=cabecalhos, data=dados_brutos)
            if resposta.status_code == 200:
                lista_jogos = resposta.json().get("hits", [])

                for jogo in lista_jogos:
                    nome = jogo.get("name", "Nome desconhecido")
                    id_jogo = jogo.get("prod_id", "")
                    nome_seo = jogo.get("seo_name", "")

                    slug = gerar_slug(nome)
                    link_img = f"https://gaming-cdn.com/images/products/{id_jogo}/271x377/{nome_seo}-cover.jpg"

                    try:
                        preco_num = float(jogo.get("price_eur", 0))
                    except:
                        preco_num = 0.0
                    
                    if slug not in bd_jogos:
                        bd_jogos[slug] = {
                            "nome": nome,
                            "imagem": link_img,
                            "ofertas": {}
                        }
                    bd_jogos[slug]["ofertas"]["Instant Gaming"] = {
                        "preco": preco_num,
                        "desconto": jogo.get("discount", 0)
                    }
            time.sleep(1)
        except Exception as e:
            print(f"Erro na página {num_pag}: {e}")
    
    return bd_jogos

def nintendo(nome_jogo):
    url_busca = f"https://searching.nintendo-europe.com/pt/select?q={nome_jogo}&fq=type%3AGAME%20AND%20((playable_on_txt%3A%22HAC%22))&rows=1&wt=json"
    cabecalhos= {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    try:
        resposta_busca = requests.get(url_busca, headers=cabecalhos)
        if resposta_busca.status_code == 200:
            docs = resposta_busca.json().get("response", {}).get("docs", [])
            if not docs: return None

            lista_ids = docs[0].get("nsuid_txt", [])
            if not lista_ids: return None
            
            nsuid = lista_ids[0]
            url_preco = f"https://api.ec.nintendo.com/v1/price?country=PT&lang=pt&ids={nsuid}"
            resposta_preco = requests.get(url_preco, headers=cabecalhos)
            if resposta_preco.status_code == 200:
                lista_precos = resposta_preco.json().get("prices", [])
                if not lista_precos: return None

                info = lista_precos[0]
                if "discount_price" in info:
                    preco = float(info["discount_price"]["raw_value"])
                    preco_normal = float(info["regular_price"]["raw_value"])
                    desconto = int(((preco_normal - preco) / preco_normal) * 100)
                else:
                    preco = float(info["regular_price"]["raw_value"])
                    desconto = 0
                
                return {"preco": preco, "desconto": desconto}
    except Exception:
        pass
    
    return None


def scraper():
    bd_final = instant(paginas=10)
    total_jogos = len(bd_final)
    count = 0
    
    for slug, info in bd_final.items():
        count +=1
        oferta_nintendo = nintendo(info['nome'])
        if oferta_nintendo:
            bd_final[slug]["ofertas"]["Nintendo eShop"] = oferta_nintendo
        
        time.sleep(0.3)

    with open('jogos.json', 'w', encoding='utf-8') as f:
        json.dump(bd_final, f, indent=4, ensure_ascii=False)

if __name__ == "__main__":
    scraper()