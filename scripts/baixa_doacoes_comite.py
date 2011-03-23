import urllib
import BeautifulSoup
import csv
import os

despesa_url = 'http://spce2010.tse.jus.br/spceweb.consulta.receitasdespesas2010/exportaReceitaCsvComite.action?'
receita_url = 'http://spce2010.tse.jus.br/spceweb.consulta.receitasdespesas2010/exportaDespesaCsvComite.action?'

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

comites = loadCsv('comite.csv')

if not os.path.isdir('./archive/despesa/comite/'):
	os.mkdir('./archive/despesa/comite/')
if not os.path.isdir('./archive/receita/comite/'):
	os.mkdir('./archive/receita/comite/')

for comite in comites:
	url = despesa_url + 'sqComiteFinanceiro=' + comite['id'] + '&sgUe=' + comite['comite_estado']
	diretorio = './archive/despesa/comite/' + comite['comite_estado'] + '/'
	arquivo = diretorio + comite['id'] + '.csv'	
	if not os.path.isdir(diretorio):
		os.mkdir(diretorio)
	if not os.path.isfile(arquivo):
		download(url,arquivo)
	print 'baixando despesa ' + comite['id']

	url = receita_url + 'sqComiteFinanceiro=' + comite['id'] + '&sgUe=' + comite['comite_estado']
	diretorio = './archive/receita/comite/' + comite['comite_estado'] + '/'
	arquivo = diretorio + comite['id'] + '.csv'	
	if not os.path.isdir(diretorio):
		os.mkdir(diretorio)
	if not os.path.isfile(arquivo):
		download(url,arquivo)
	print 'baixando receita ' + comite['id']
