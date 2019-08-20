

def sortByKey(data={},key=None):
    if key:
        data = sorted(data, key=lambda a: int(a[key]),reverse=True)
        return data
    return None

def filterByKeyword(data={},keyword=None,field='nome'):
    '''
        Filtra um campo com base em uma ou mais palavras chaves.
    '''
    if keyword:
        if type(keyword) is list:
            for key in keyword:
                data = [item for item in data if field in item and key.lower() in item[field].lower()]
        else:
            data = [item for item in data if field in item and keyword.lower() in item[field].lower()]

    return data
