import sqlite3

def loadEmpresas(arquivo):
	conn = sqlite3.connect(arquivo)
	c = conn.cursor()
	c.execute('select * from swdata')
	results = c.fetchall()
	c.close()
	return results

empresas = loadEmpresas('data/empresas.sqlite')

conn = sqlite3.connect('data/doacoes.sqlite')
c = conn.cursor()
conn2 = sqlite3.connect('data/tselookup.sqlite')
c2 = conn2.cursor()
counter = 0
for empresa in empresas:
	teste = c.execute('''select * from swdata where cnpj == ?''', [empresa[0]])
	hits = teste.fetchall()	
	#for hit in hits:
		#c2.execute('''insert into doacoes values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', hit)
	#	print 'match: ' + empresa[0]
	#	counter = counter + 1
	if (hits):
		c2.execute('''insert into empresas values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', empresa)
print str(counter) + ' matches'
c.close()
c2.close()
conn2.commit()
