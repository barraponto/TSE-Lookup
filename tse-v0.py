import re
import urllib
from BeautifulSoup import BeautifulSoup
import csv
import urllib
import sqlite3
import web

# retrieve a page
#csv_doacoes = 'data/doacoes-presidenciais.csv'
#csv_empresas = 'lista-empresas.csv'
database = 'data/empresas.sqlite'
db_doacoes = 'data/doacoes.sqlite'

def loadCsv(url):
	csv_file = open(url)
	lines = csv_file.readlines()
	clist = list(csv.reader(lines))
	header = clist.pop(0)   # set 'header' to be the first row of the CSV file
	result = [ dict(zip(header, row))  for row in clist ]
	return result	

def loadEmpresas(arquivo):
	conn = sqlite3.connect(arquivo)
	c = conn.cursor()
	c.execute('select nome, cnpj from swdata')
	results = c.fetchall()	
	c.close()
	return results

def loadDoacoes(arquivo):
	conn = sqlite3.connect(arquivo)
	c = conn.cursor()
	c.execute('select name, cnpj, value, candidate, date, party from swdata')
	results = c.fetchall()	
	c.close()
	return results

def checkDonations(hit, doacoes):
	lista = []
	for empresa in doacoes:
		if hit[1] == empresa[1]:
			lista.append(empresa)
	return lista		

def checkStory(url, empresas, doacoes):
    html = urllib.urlopen(url)
    print 'Carregando pagina...'
    soup = BeautifulSoup(html)
    lista = []
    for empresa in empresas:
	if (empresa[0] != ''):
		hit = soup.find(text=re.compile(empresa[0]))
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
		doacoes = loadDoacoes(db_doacoes)
		empresas = loadEmpresas(db_empresas)
		lista = []
		i = web.input(url='')		
		if (i.url):		
			lista = checkStory(i.url, empresas, doacoes)
		else:
			lista = []
		return render.index(lista, i.url)

class 


if __name__ == "__main__": app.run()

