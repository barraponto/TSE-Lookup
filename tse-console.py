import sqlite3

def loadEmpresas(arquivo):
	conn = sqlite3.connect(arquivo)
	c = conn.cursor()
	c.execute('select cnpj, nome from swdata')
	results = c.fetchall()	
	c.close()
	return results

empresas = loadEmpresas('data/empresas.sqlite')

conn = sqlite3.connect('data/doacoes.sqlite')
c = conn.cursor()
counter = 0
for empresa in empresas:
	teste = c.execute('''select name from swdata where cnpj == ?''', [empresa[0]])
	hits = teste.fetchall()	
	if (hits):
		print 'match: ' + empresa[1]
		counter = counter + 1
print str(counter) + ' matches'
c.close()
