import urllib
import BeautifulSoup
import csv
import os

despesa_url = 'http://spce2010.tse.jus.br/spceweb.consulta.receitasdespesas2010/exportaPartidoCsvpartido.action?'
receita_url = 'http://spce2010.tse.jus.br/spceweb.consulta.receitasdespesas2010/exportaReceitaCsvpartido.action?'


def loadCsv(filename):
	csv_file = open(filename)
	lines = csv_file.readlines()
	clist = list(csv.reader(lines))
	header = clist.pop(0)
	result = [ dict(zip(header, row))  for row in clist ]
	return result

def download(url, filename):
	webFile = urllib.urlopen(url)
	localFile = open(filename, 'w')
	localFile.write(webFile.read())
	webFile.close()
	localFile.close()

partidos = loadCsv('partido.csv')

if not os.path.isdir('./archive/despesa/partido/'):
	os.mkdir('./archive/despesa/partido/')
if not os.path.isdir('./archive/receita/partido/'):
	os.mkdir('./archive/receita/partido/')

for partido in partidos:
	url = despesa_url + 'sqpartidoFinanceiro=' + partido['id'] + '&sgUe=' + partido['partido_estado']
	diretorio = './archive/despesa/partido/' + partido['partido_estado'] + '/'
	arquivo = diretorio + partido['id'] + '.csv'	
	if not os.path.isdir(diretorio):
		os.mkdir(diretorio)
	if not os.path.isfile(arquivo):
		download(url,arquivo)
	print 'baixando receita ' + partido['id']

	url = receita_url + 'sqpartidoFinanceiro=' + partido['id'] + '&sgUe=' + partido['partido_estado']
	diretorio = './archive/receita/partido/' + partido['partido_estado'] + '/'
	arquivo = diretorio + partido['id'] + '.csv'	
	if not os.path.isdir(diretorio):
		os.mkdir(diretorio)
	if not os.path.isfile(arquivo):
		download(url,arquivo)
	print 'baixando despesa ' + partido['id']
