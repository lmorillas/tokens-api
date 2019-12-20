# pylint: disable=C0111, E0401
""" API Entry Point """

from hug_middleware_cors import CORSMiddleware
import spacy
from spacy import displacy
from spacy_spanish_lemmatizer import SpacyCustomLemmatizer
try:
    from images import get_image, get_images
except:
    from .images import get_image, get_images
import hug


print("Loading...")
MODELS = {
    "en": spacy.load("en_core_web_sm"),
    "es": spacy.load('train_es', parse=True, tag=True, entity=True),
    #"en_core_web_lg": spacy.load("en_core_web_lg"),
    #"es_core_news_sm": spacy.load("es_core_news_sm"),
    #"es_core_news_md": spacy.load("es_core_news_md"),
}
nlp_es  = MODELS['es']
nlp_en = MODELS['en']
lemmatizer = SpacyCustomLemmatizer()
nlp_es.add_pipe(lemmatizer, name="lemmatizer", after="tagger")
 
print("Loaded!")


api = hug.API(__name__)
api.http.base_url = '/api' 
api.http.output_format = hug.output_format.pretty_json
#api.http(on_invalid=hug.redirect.not_found)
#api.http.base_url('/api')
#api.http.add_middleware(CORSMiddleware(api))

def fila(datos, color=None):
    if color != None:
        color = datos[color]
    else: color=''
    return '<tr class="{}">{}</tr>'.format(color, 
        ''.join(["<td>{}</td>".format(c) for c in datos]) 
        )
    
def creatabla(columnas, filas, color=None):
    t = '''<table class="responsive-table">
              <thead>
                <tr>
                {}
                </tr>
              </thead>
            {}
            </table>
        '''
    coltext = ''.join(['<th data-field="{}">{}</th>'.format(c, c) for c in columnas])
    filastext = ''.join([fila(f, color) for f in filas])
    return t.format(coltext, filastext)


def tolemma(x, lang):
    if lang == 'en' and x.lemma_ == '-PRON-':
        return x.text
    else:
        return x.lemma_

def analyze_text(text, lang):
    if lang == "en":
        doc = nlp_en(text)
    else:
        doc = nlp_es(text)
    return doc

def word_type(pos, lang):
    if lang == 'en':
        pass
    if lang == 'es':
        pass

@hug.local()
@hug.post("/vtokens", examples="text=Por la mañana me lavo los dientes&lang=es", 
    on_invalid=hug.redirect.not_found)
def vtokens(text: hug.types.text, lang="es", hug_timer=3):
    '''Returns json para visualización de análisis de frases:
        tokens: svg
        time: float
        tabla: html
    '''
    
    doc = analyze_text(text, lang)

    html = displacy.render(doc, style='dep')

    spacy_pos_tagged = [(word, ', '.join(word.tag_.split('|')), word.pos_, word.lemma_) for word in doc]
    #df = pd.DataFrame(spacy_pos_tagged, columns=['Word', 'POS tag', 'Tag type', 'Lemma'])
    columns=['Word', 'POS tag', 'Tag type', 'Lemma']
    cols_imgs = ['text', 'images', 'lemma', 'pos', 'tag']

    images = [dict(zip(cols_imgs, (w.text, get_images(tolemma(w, lang),  lang), w.lemma_, w.pos_, w.tag_))) for w in doc if not w.is_punct and not w.is_space]

    return {'tokens': html,
            'time': float(hug_timer),
            #'tabla': df.to_html(classes=["responsive-table  striped table-bordered", "table-striped", "table-hover"])}
            'tabla': creatabla(columns, spacy_pos_tagged, 2),
            'images': images
    }
   
#@hug.get("/tokens", examples="text=Por la mañana me lavo los dientes&lang=es", 
#    on_invalid=hug.redirect.not_found)

def tokens(text: hug.types.text, lang="es", hug_timer=3):
    '''Returns json para con tags y lemma'''
    if lang == "en":
        doc = nlp_en(text)
    else:
        doc = nlp_es(text)
    claves = ['word', 'tags', 'pos', 'lemma']
    spacy_pos_tagged = [ dict( zip( claves, (
            word.__str__(), ', '.join(word.tag_.split('|')), word.pos_, word.lemma_) ))
            for word in doc]

    return {'tokens': spacy_pos_tagged }
   

@hug.local()
@hug.post("/tokensToImages", examples="text=Por la mañana me lavo los dientes&lang=es", 
    on_invalid=hug.redirect.not_found)
def tokenstoimages(text: hug.types.text, lang="es", hug_timer=3):
    '''Returns json para con tags y lemma'''
    if lang == "en":
         doc = nlp_en(text)
    else:
        doc = nlp_es(text)
    claves = ['word', 'tags', 'pos', 'lemma', 'images']
    spacy_pos_tagged = [ dict( zip( claves, (
            word.text, word.tag_, word.pos_, word.lemma_, get_images(tolemma(word, lang), lang)) ))
            for word in doc]

    return {'tokens': spacy_pos_tagged }


'''
if __name__ == "__main__":
    pass

    import waitress

    app = hug.API(__name__)
    app.http.add_middleware(CORSMiddleware(app))
    waitress.serve(__hug_wsgi__, listen='*:8000')
'''
