# ~#~ coding: UTF-8 ~#~

# Modules ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
import urllib2
from cStringIO import StringIO

from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


# Functions ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def convert(url, pages=None):
    assert isinstance(url, basestring)
    assert pages == None or isinstance(pages, list)

    rscmng = PDFResourceManager()
    retstr = StringIO()
    device = TextConverter(rscmng, retstr, codec='utf-8', laparams=LAParams())
    web_page = urllib2.urlopen(urllib2.Request(url))
    fp = StringIO(web_page.read())
    interpreter = PDFPageInterpreter(rscmng, device)

    pdf_pages = PDFPage.get_pages(
        fp,
        set(pages if pages != None else []),
        maxpages=0,
        password='',
        caching=True,
        check_extractable=True
    )

    for page in pdf_pages:
        interpreter.process_page(page)

    result = retstr.getvalue()

    fp.close()
    web_page.close()
    device.close()
    retstr.close()

    return result
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
