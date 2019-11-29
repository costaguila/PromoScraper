import multiprocessing as mp
from datetime import datetime
from utils import filters
import time

from scrapers.sections import *
from scrapers import pelando

# Tempo para esperar entre requisições
STANDARD_DELAY=15

def InParallel(urls=[],alvo=None):
    queue = mp.Queue()
    processes = [mp.Process(target=alvo,args=(section,queue)) for section in urls]
    # start processes
    print("Iniciando {} scrapers.".format(len(processes)))
    print("DELAY PADRÃO(para não sobrecarregar os servidores,\
    se quiser diminuir altere no arquivo scrape.py): {} SEGUNDOS".format(STANDARD_DELAY))
    inicio = datetime.now()
    for p in processes:
        p.daemon = True
        p.start()
        time.sleep(STANDARD_DELAY)
    # exit processes
    for p in processes:
        p.join()
    fim = datetime.now()
    print("Fim de execucao para {} scrapers.".format(len(processes)))
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
    to_scrape = sectionSelect([SECTION_VIDEOGAMES,SECTION_COMPUTADORES], pelando.ALL_SECTIONS)
    temp = []
    query = ['controle']
    for page in to_scrape:
        for i in range(1,7):
            temp.append(page+"?page={}".format(i))
    to_scrape = temp
    data = InParallel(to_scrape,pelando.scrapePelandoSection)
    print("\n######\nFiltrando o campo nome por(case insensitive):\n{}\n######".format(query))
    data = filters.filterByKeyword(data,query)
    data = filters.sortByKey(data,"temperatura")
    print("Quantidade de resultados após filtragem: {}".format(len(data)))
    for item in data:
        print("------------------------------------------")
        print("ID: {}\nNome: {}\tSecao: {}\nTemperatura:{}\tPreco:{}".format(item['id'],item['nome'],item['section'],item['temperatura'],item['valor']))
