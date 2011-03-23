import urllib
import BeautifulSoup
import csv
import os

despesa_url = 'http://spce2010.tse.jus.br/spceweb.consulta.receitasdespesas2010/exportaReceitaCsvCandidato.action?'
receita_url = 'http://spce2010.tse.jus.br/spceweb.consulta.receitasdespesas2010/exportaDespesaCsvCandidato.action?'

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

candidatos = loadCsv('candidatos.csv')

if not os.path.isdir('./archive/despesa/candidato/'):
	os.mkdir('./archive/despesa/candidato/')
if not os.path.isdir('./archive/receita/candidato/'):
	os.mkdir('./archive/receita/candidato/')

for candidato in candidatos:
	url = despesa_url + 'sqCandidato=' + candidato['id'] + '&sgUe=' + candidato['candidato_estado']
	diretorio = './archive/despesa/candidato/' + candidato['candidato_estado'] + '/'
	arquivo = diretorio + candidato['id'] + '.csv'	
	if not os.path.isdir(diretorio):
		os.mkdir(diretorio)
	if not os.path.isfile(arquivo):
		download(url,arquivo)
	print 'baixando despesa ' + candidato['id']

	url = receita_url + 'sqCandidato=' + candidato['id'] + '&sgUe=' + candidato['candidato_estado']
	diretorio = './archive/receita/candidato/' + candidato['candidato_estado'] + '/'
	arquivo = diretorio + candidato['id'] + '.csv'	
	if not os.path.isdir(diretorio):
		os.mkdir(diretorio)
	if not os.path.isfile(arquivo):
		download(url,arquivo)
	print 'baixando receita ' + candidato['id']
