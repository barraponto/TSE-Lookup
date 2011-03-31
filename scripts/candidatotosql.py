import csv
import sqlite3

def loadCsv(filename):
	csv_file = open(filename)
	lines = csv_file.readlines()
	clist = list(csv.reader(lines, delimiter=";"))
	header = clist.pop(0)
	return clist

def createCandidateTable(conn):
	c = conn.cursor()
	c.execute('''create table swdata (
	name TEXT,
	cnpj TEXT,
	date TEXT,
	donation_number TEXT,
	value TEXT,
	type TEXT,
	candidate TEXT,
	candidate_number TEXT,
	candidature TEXT,
	party TEXT,
	state TEXT)''')
	conn.commit()
	c.close()

candidatos = loadCsv('convert.csv')
conn = sqlite3.connect('candidato.sqlite')
createCandidateTable(conn)
c = conn.cursor()
for candidato in candidatos:
	candidato.pop(11)
	candidato.pop(11)
	candidato_u=[unicode(x, 'iso-8859-1') for x in candidato]
	print 'Inserting ' + candidato[0]
	c.execute('''insert into swdata values (?, ?, ?, ?, ?, ?, ?, ?, ? ,? ,?)''', candidato_u)
conn.commit()
c.close()
