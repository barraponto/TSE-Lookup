import re
import urllib
from BeautifulSoup import BeautifulSoup
import csv
import urllib

import web

# retrieve a page
starting_url = 'http://oglobo.globo.com/economia/miriam/posts/2011/03/21/pib-cresceu-0-4-em-janeiro-calcula-itau-unibanco-370125.asp'
csv_doacoes = 'doacoes-presidenciais.csv'
csv_empresas = 'lista-empresas.csv'

def loadCsv(url):
	csv_file = open(url)
	lines = csv_file.readlines()
	clist = list(csv.reader(lines))
	header = clist.pop(0)   # set 'header' to be the first row of the CSV file
	result = [ dict(zip(header, row))  for row in clist ]
	return result	

def checkDonations(hit, doacoes):
	lista = []
	for empresa in doacoes:
		if hit['cnpj'] == empresa['cnpj']:
			lista.append(empresa)
	return lista		

def checkStory(url, empresas, doacoes):
    html = urllib.urlopen(url)
    print 'Carregando pagina...'
    soup = BeautifulSoup(html)
    lista = []
    for empresa in empresas:  
	if (empresa['real_name'] != ''):
		hit = soup.find(text=re.compile(empresa['real_name']))
        	if (hit):
			lista = lista + checkDonations(empresa, doacoes)
    return lista

#web
render = web.template.render('templates/')

urls = (
	'/', 'index'
)


app = web.application(urls, globals())

class index:
	def GET(self):
		doacoes = loadCsv(csv_doacoes)
		empresas = loadCsv(csv_empresas)
		lista = []
		i = web.input(url=starting_url)		
		lista = checkStory(i.url, empresas, doacoes)
		return render.index(lista, i.url)

if __name__ == "__main__": app.run()

