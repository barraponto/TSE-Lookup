import re
import urllib
from BeautifulSoup import BeautifulSoup
import csv
import urllib
import sqlite3
import web
import json

# retrieve a page
#csv_doacoes = 'data/doacoes-presidenciais.csv'
#csv_empresas = 'lista-empresas.csv'
database = 'data/tselookup.sqlite'
db_doacoes = 'data/doacoes.sqlite'

def connectDb(arquivo):
	conn = sqlite3.connect(arquivo)
	return conn

def loadEmpresas(conn):
	c = conn.cursor()
	c.execute('select nome, cnpj from empresas')
	results = c.fetchall()
	c.close()
	return list(results)

def checkDonations(conn, empresas):
	results = []
	for empresa in empresas:
		c = conn.cursor()	
		result = c.execute('''select name, cnpj, value, candidate, date, party from doacoes where cnpj=?''', [empresa[1]])
		results = results + [result.fetchall()]
		c.close()
	return results

def checkStory(url, empresas):
	html = urllib.urlopen(url)
	print 'Carregando pagina...'
	soup = BeautifulSoup(html)
	results = []
	for empresa in empresas:
		hit = soup.find(text=re.compile(empresa[0]))
		if (hit):
			results = results + [empresa]
	return list(results)

def spitJason(lista, url):
	entries = []
	for empresa in lista:
		donations = []
		total_donation = 0
		for doacao in empresa:
			donation = {
			'value' : int(doacao[2].encode('utf-8').translate(None,'R$.,')),				
			'candidate' : doacao[3],
			'date' : doacao[4],
			'party' : doacao[5]
			}
			donations = donations + [donation]
			total_donation = donation['value'] + total_donation
		entry = {
			'url' : url,
			'company' : {
			'name' : empresa[0][0],
			'donation' : donations,
			'total_donation' : total_donation
				}
			}
		entries = entries + [entry]
	return json.dumps(entries, indent=2)

#web
render = web.template.render('templates/')

urls = (
	'/', 'index',
	'/json', 'jason'
)


app = web.application(urls, globals())

class index:
	def GET(self):
		conn = connectDb(database)		
		empresas = loadEmpresas(conn)
		lista = []
		i = web.input(url='')		
		if (i.url):		
			hits = checkStory(i.url, empresas)
			lista = checkDonations(conn, hits)
		else:
			lista = []
		return render.index(lista, i.url)

class jason:
	def GET(self):
		conn = connectDb(database)		
		empresas = loadEmpresas(conn)
		lista = []
		i = web.input(url='')		
		if (i.url):		
			hits = checkStory(i.url, empresas)
			lista = checkDonations(conn, hits)
		else:
			lista = []
		return spitJason(lista, i.url)

if __name__ == "__main__": app.run()

