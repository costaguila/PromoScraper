SECTION_COMPUTADORES = 'computadores'
SECTION_TECEESCRITORIO = 'tecnologia_escritorio'
SECTION_SMARTPHONES = 'smarphones'
SECTION_LIVROS = 'livros'
SECTION_VIDEOGAMES = 'videogames'


def sectionSelect(sections=[],scraper_sections={}):
    '''
        Recebe um conjunto de chaves e um dicionario com  URLs.
        Retorna uma lista de URLs que correspondem as chaves.
    '''
    keys = scraper_sections.keys()
    to_crawl = []

    for item in sections:
        if item.lower() in keys:
            to_crawl.append(scraper_sections[item.lower()])

    return to_crawl
