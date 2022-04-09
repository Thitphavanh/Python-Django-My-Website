# writedb.py
import sqlite3
import csv
conn = sqlite3.connect('db.sqlite3')
c = conn.cursor()


def writetodb(token, approved, user_id):
	# write data to verifyemail table
	with conn:
		c.execute("""INSERT INTO myapp_verifyemail (id, token, approved, user_id) VALUES (?,?,?,?)""",
			(None, token, approved, user_id))
	conn.commit() # save to database
	print('Completed')

# writetodb('ajfjkahkfakhkbfdas',0,16)

# -------read csv--------
with open('newtoken.csv', newline = '', encoding = 'utf-8') as f:
	file_reader = csv.reader(f)
	data = list(file_reader)


for t,a,u in data:
	print(t,a,u)
	writetodb(t, int(a), int(u))
	# new = VerifyEmail()
	# new.user = User.objects.get(id=int(u))
	# new.token = t 
	# new.approved = bool(int(a))
	# new.save()