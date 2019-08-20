import requests
import multiprocessing as mp
from datetime import datetime
from bs4 import BeautifulSoup
from utils import filters

SITE_PELANDO_COMPUTADORES = "https://www.pelando.com.br/grupo/computadores-e-informatica"
SITE_PELANDO_TECEESCRITORIO = "https://www.pelando.com.br/grupo/tecnologia-e-escritorio"
SITE_PELANDO_SMARTPHONES = "https://www.pelando.com.br/grupo/celulares-e-smartphones"
SITE_PELANDO_LIVROS = "https://www.pelando.com.br/grupo/livros"
SITE_PELANDO_VIDEOGAMES = "https://www.pelando.com.br/grupo/videogames"

SECTION_COMPUTADORES = 'computadores'
SECTION_TECEESCRITORIO = 'tecnologia_escritorio'
SECTION_SMARTPHONES = 'smarphones'
SECTION_LIVROS = 'livros'
SECTION_VIDEOGAMES = 'videogames'

ALL_SECTIONS = {
    SECTION_COMPUTADORES: SITE_PELANDO_COMPUTADORES,
    SECTION_TECEESCRITORIO: SITE_PELANDO_TECEESCRITORIO,
    SECTION_SMARTPHONES: SITE_PELANDO_SMARTPHONES,
    SECTION_LIVROS: SITE_PELANDO_VIDEOGAMES,
    SECTION_VIDEOGAMES: SITE_PELANDO_LIVROS
}

def sectionSelect(sections=[SECTION_COMPUTADORES,SECTION_TECEESCRITORIO,SECTION_SMARTPHONES,SECTION_LIVROS,SECTION_VIDEOGAMES]):
    keys = ALL_SECTIONS.keys()
    to_crawl = []

    for item in sections:
        if item.lower() in keys:
            to_crawl.append(ALL_SECTIONS[item.lower()])

    return to_crawl

def crawlPelandoSection(section=None,output=None):
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


def crawlInParallel(urls=[]):
    queue = mp.Queue()
    processes = [mp.Process(target=crawlPelandoSection,args=(section,queue)) for section in urls]
    # start processes
    print("Iniciando {} crawlers.".format(len(processes)))
    inicio = datetime.now()
    for p in processes:
        p.daemon = True
        p.start()
    # exit processes
    for p in processes:
        p.join()
    fim = datetime.now()
    print("Fim de execucao para {} crawlers.".format(len(processes)))
    print("Calculando estatisticas...\n")
    duration = fim - inicio
    results = [queue.get() for p in processes]
    #flatten
    results = [item for sublista in results for item in sublista]
    print("Tempo de duracao(segundos): {}".format(duration.total_seconds()))
    print("Quantidade de resultados: {}".format(len(results)))
    #print("\n##\tRESULTADOS\t##")
    #print(results)
    return results

if __name__ == "__main__":
    to_crawl = sectionSelect([SECTION_COMPUTADORES,SECTION_TECEESCRITORIO,SECTION_SMARTPHONES])
    temp = []
    query = ['SSD','KiNgsTon']
    for page in to_crawl:
        for i in range(1,5):
            temp.append(page+"?page={}".format(i))
    to_crawl = temp
    data = crawlInParallel(to_crawl)
    print("\n######\nFiltrando o campo nome por(case insensitive):\n{}\n######".format(query))
    data = filters.filterByKeyword(data,query)
    data = filters.sortByKey(data,"temperatura")
    print("Quantidade de resultados após filtragem: {}".format(len(data)))
    for item in data:
        print("------------------------------------------")
        print("ID: {}\nNome: {}\tSecao: {}\nTemperatura:{}\tPreco:{}".format(item['id'],item['nome'],item['section'],item['temperatura'],item['valor']))
