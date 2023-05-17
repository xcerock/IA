import re
import random
from collections import Counter

TEXT = open('corrector ortografico\\textos\dict_en.txt', 'r', encoding='utf-8').read()
#print(len(TEXT))

def tokens(text):
    '''
    lista todas las palabras tokenizadas(letras concatenadas)
    en un texto. Normaliza a minusculas.
    '''
    #return re.findall('[a-záéíóúñü]+', text.lower())
    return re.findall('[a-z]+', text.lower())

def sample(bag, n = 10):
    '''
    toma una muestra aleatoria de n elementos de una bolsa de palabras
    '''
    return ' '.join(random.choice(bag) for _ in range(n))

WORDS = tokens(TEXT)

#print(sample(WORDS))

COUNTS = Counter(WORDS)

def correct(word):
    '''
    corrige la palabra de entrada
    '''
    candidates = (known(edits0(word)) or 
                  known(edits1(word)) or 
                  known(edits2(word)) or 
                  [word])
    
    return max(candidates, key=COUNTS.get)

def known(words):
    '''
    retorna las palabras que estan en el diccionario
    '''
    return {w for w in words if w in COUNTS}

def edits0(word):
    '''
    retorna todas las palabras que estan a una distancia de edicion
    de la palabra de entrada
    '''
    return {word}

def edits1(word):
    '''

    '''
    pairs = splits(word)
    deletes = [a + b[1:] for (a, b) in pairs if b]
    transposes = [a + b[1] + b[0] + b[2:] for (a, b) in pairs if len(b) > 1]
    replaces = [a + c + b[1:] for (a, b) in pairs for c in alphabet if b]
    inserts = [a + c + b for (a, b) in pairs for c in alphabet]

    return set(deletes + transposes + replaces + inserts)

def edits2(word):
    '''
    retorna todas las palabras que estan a dos distancias de edicion
    de la palabra de entrada
    '''
    return {e2 for e1 in edits1(word) for e2 in edits1(e1)}

def splits(word):
    '''
    retorna una lista de todas las posibles divisiones de una palabra
    '''
    return [(word[:i], word[i:]) for i in range(len(word) + 1)]

alphabet = 'abcdefghijklmnopqrstuvwxyz'

def correct_text(text):
    '''
    corrige todas las palabras de un texto, y retorna el texto corregido
    '''
    return re.sub('[a-zA-Z]+', correct_match, text)

def correct_match(match):
    '''
    corrige una palabra de un texto
    '''
    word = match.group()
    return case_of(word)(correct(word.lower()))

def case_of(text):
    '''
    retorna la funcion que convierte un texto a mayusculas o minusculas
    '''
    return str.upper if text.isupper() else str.lower if text.islower() else str.title if text.title() else str

print(list(map(correct, tokens('speech eis nop good'))))

#print(COUNTS['narración'])