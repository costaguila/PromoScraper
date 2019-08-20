import requests
from bs4 import BeautifulSoup

from .sections import *

SITE_PELANDO_COMPUTADORES = "https://www.pelando.com.br/grupo/computadores-e-informatica"
SITE_PELANDO_TECEESCRITORIO = "https://www.pelando.com.br/grupo/tecnologia-e-escritorio"
SITE_PELANDO_SMARTPHONES = "https://www.pelando.com.br/grupo/celulares-e-smartphones"
SITE_PELANDO_LIVROS = "https://www.pelando.com.br/grupo/livros"
SITE_PELANDO_VIDEOGAMES = "https://www.pelando.com.br/grupo/videogames"

ALL_SECTIONS = {
    SECTION_COMPUTADORES: SITE_PELANDO_COMPUTADORES,
    SECTION_TECEESCRITORIO: SITE_PELANDO_TECEESCRITORIO,
    SECTION_SMARTPHONES: SITE_PELANDO_SMARTPHONES,
    SECTION_LIVROS: SITE_PELANDO_VIDEOGAMES,
    SECTION_VIDEOGAMES: SITE_PELANDO_LIVROS
}

def scrapePelandoSection(section=None,output=None):
    "Receve uma URL e um objeto do tipo Queue da biblioteca multiprocessing(padrão). Os resultidas são salvos na Queue."
    request_phase_success = True
    result = []
    try:
        source = requests.get(section).text
        soup = BeautifulSoup(source,'lxml')
        promotion = soup.select('article.thread.thread--type-card')
        section_name = section.split('/')[-1].split('?')[0]
    except Exception as e:
        print("Error during request phase")
        print(e)
        request_phase_success = False

    if request_phase_success:
        for item in promotion:
            try:
                temperatura = item.select("span.vote-temp")[0].text.split('°')[0].strip()
                if temperatura.lower() != "super quente!":
                    id = item.get('id')
                    titulo = item.select("a.thread-link.thread-title--card")[0].text.strip()
                    valor = item.select("span.thread-price")[0].text.strip()

                    result.append({"id": id,"nome": titulo, "valor": valor, "temperatura": temperatura, "section": section_name})
            except IndexError as e:
                # Pula itens sem um dos campos
                pass
            except Exception as e:
                print("Erro:{}  em {}".format(e,section))

    output.put(result)
    print("## {} FINALIZOU ##".format(section))
