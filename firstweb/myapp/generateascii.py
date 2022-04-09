# generateascii.py
import random
def GenerateToken(domain = 'http'):
	allchr = [chr(i) for i in range(65,91)]
	allchr.extend([chr(i) for i in range(97,123)])
	allchr.extend([str(i) for i in range(10)])
	email_token = ''
	for i in range(40):
		email_token += random.choice(allchr)

	url = domain + email_token
	# print(url)
	return url
gurl = GenerateToken()


'''allchr = []
for i in range(65,91):
	allchr.append(chr(i))
for i in range(97,123):
	allchr.append(chr(i))
for i in range(10):
	allchr.append(str(i))
print(allchr)
allchr = [chr(i) for i in range(65,91)]
allchr.extend([chr(i) for i in range(97,123)])
allchr.extend([str(i) for i in range(10)])
print(allchr)'''
