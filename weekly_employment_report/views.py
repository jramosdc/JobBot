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
import python_usdol
import json,datetime,re

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

   #DOLAPI
    conn = python_usdol.Connection(token='bf7867cd-4297-40ec-8fcb-f03597aa6dfe', secret='appl')  

    data = conn.fetch_data("Statistics/OUI_InitialClaims","unemploymentInsuranceInitialClaims", skip=2508)

    jsondata= json.dumps(data)

    jsondata1= json.loads(jsondata)

    #cleandataDOLAPI
    regex= r'[a-zA-Z()/]+'
    pat= re.compile(regex)
    ultimo=jsondata1[-1]['seasonallyAdjustedInitialClaims']
    results = []
    fecha=[]
    for i in reversed(jsondata1):
        time=i['week']
        timeregex= float(pat.sub('',time))
        timeread= datetime.datetime.fromtimestamp(timeregex/1000.0).strftime("%B %d, %Y")
        figure=i['seasonallyAdjustedInitialClaims']
        results.append(int(figure))
        fecha.append(timeread) 
    if ultimo>results[1]:
        linea0= ' Higher than the previous week.'
    else:
        match=next(obj for obj in results if obj<ultimo)
        position=results.index(match)
        linea0=u' '.join([' The lowest since the week of']+[fecha[position]]+['.'])
    # Procesar
    # Procesar
    tokenizer = nltk.data.load('nltk:tokenizers/punkt/english.pickle')
    lineas = tokenizer.tokenize(text)
    textlinea0=u' '.join(lineas[2:100])
    lineas=tokenizer.tokenize(textlinea0)
    palabras = nltk.word_tokenize(textlinea0)
    cifra1 = u' '.join(palabras[25:36])
    cifra2 = u' '.join(palabras[20:24]+[', according to data of the Department of Labor.'])+linea0
    linea1 = u' '.join(palabras[7:33]).replace(u' ,', u',')
    linea2 = u' '.join(lineas[2:3])
    linea3 = u' '.join(lineas[5:6])

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
