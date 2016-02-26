# ~#~ coding: UTF-8 ~#~

u"""
En este archivo se encuentran las vistas de la aplicación.
"""

# Modules ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
import gspread
import nltk.data
from flask import render_template
from flask import request
from oauth2client.client import SignedJwtAssertionCredentials

from . import app
from . import helpers
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


# Views ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
@app.route('/', methods=['GET', 'POST'])
def index():
    text = helpers.convert('http://www.dol.gov/ui/data.pdf', pages=[0])

    if request.method == 'GET':
        return render_template('show.html', text=text)

    # Autorizar
    gc = gspread.authorize(SignedJwtAssertionCredentials(
        app.config['GS_AUTH']['client_email'],
        app.config['GS_AUTH']['private_key'].encode(),
        ['https://spreadsheets.google.com/feeds']
    ))

    # Procesar
    tokenizer = nltk.data.load('nltk:tokenizers/punkt/english.pickle')
    lineas = tokenizer.tokenize(text)
    palabras = nltk.word_tokenize(text)
    cifra1 = u' '.join(palabras[54:58])
    cifra2 = u' '.join(palabras[49:53]+[', according to data of the Department of Labor'])
    linea1 = u' '.join(palabras[36:62]).replace(u' ,', u',')
    linea2 = u' '.join(lineas[1:2])
    linea3 = u' '.join(lineas[4:5])

    # Obtener datos de desempleo de googlesheet
    sht1 = gc.open_by_key(app.config['SPREADSHEET_ID'])
    worksheet = sht1.get_worksheet(0)
    celda = worksheet.acell('P15').value
    linea5 = u'The last unemployment figure is {}'.format(celda)

    return render_template('show.html', **dict(
        cifra1=cifra1,
        cifra2=cifra2,
        linea1=linea1,
        linea2=linea2,
        linea3=linea3,
        linea5=linea5
    ))
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
