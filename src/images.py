import requests                                                                                                         
import json

api_kw = "https://api.arasaac.org/api/pictograms/{}/search/{}"
api_best = "https://api.arasaac.org/api/pictograms/{}/bestsearch/{}"
api_picto = "https://api.arasaac.org/api/pictograms/{}?download=false"
url_picto = "https://static.arasaac.org/pictograms/{picto}/{picto}_300.png"


def get_image(word, lang="es"):
    '''
    Returns the picto's url in 300px resolution
    '''
    busqueda = requests.get(api_kw.format(lang, word))
    if busqueda.ok:
        resultado = json.loads(busqueda.text)
        picto = resultado[0].get('_id')
        return url_picto.format(**{"picto": picto})
    return False

def get_images(word, lang="es"):
    word = word.lower()
    busqueda = requests.get(api_best.format(lang, word))

    if busqueda.ok:
        resultado = json.loads(busqueda.text)
        pictos = [ res.get('_id') for res in resultado]
        return pictos
    else:
        busqueda = requests.get(api_kw.format(lang, word))
        if busqueda.ok:
            resultado = json.loads(busqueda.text)
            pictos = [ res.get('_id') for res in resultado]
            return pictos
    return False
    

'''
Example:

{'_id': 2483,
 'created': '2007-12-14T13:01:18.000Z',
 'downloads': 0,
 'tags': [],
 'synsets': ['07763583-n'],
 'sex': False,
 'lastUpdated': '2008-07-23T12:58:09.000Z',
 'schematic': False,
 'keywords': [{'idLocution': '78.mp3',
   'keyword': 'naranja',
   'type': 2,
   'meaning': ' f. Fruto comestible del naranjo, de forma globosa y de pulpa dividida en gajos.',
   'plural': 'naranjas',
   'idKeyword': 78,
   'idLSE': 12418}],
 'categories': [],
 'violence': False}

picto = requests.get("https://api.arasaac.org/api/pictograms/{}?download=true".format(resultado[0].get('_id')))                     
open('test.png', 'wb').write(picto.content)                                                                             '''


