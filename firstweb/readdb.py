# readdb.py
import sqlite3
import csv

conn = sqlite3.connect('db.sqlite3')
c = conn.cursor()

with conn:
	c.execute("""SELECT * FROM myapp_orderpending WHERE user_id = 8""")
	data = c.fetchall()
	# data = c.fetchmany(8)
	# data = c.fetchone()
	print(data)
	for d in data:
		print(d)
		print('-----')

# -------import to CSV-------

	with open('allorder_user3.csv','w',newline = '',encoding = 'utf-8') as f:
		file_writer = csv.writer(f)
		file_writer.writerows(data)