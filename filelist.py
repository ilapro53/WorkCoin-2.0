import json

def readlist(filename):
	with open(filename, 'r') as f:  
		list = json.load(f)
	return list

def writelist(filename, list):
	with open(filename, 'w') as f:  
		json.dump(list, f)
'''
a = {'a':'12'}
writelist('rights.txt', a)
a.update({"b":'88'})
'''

#writelist('rights.txt', {'377774355':'admin'})
f = open('rights.txt', 'r')
n = f.read().replace(" ", "").replace("\n", "")
f.close()
f = open('rights.txt', 'w')
f.write(json.json(n))
f.close()
a = readlist('rights.txt')
print(readlist('rights.txt').get('377774355'))
print(a.pop('r', None))
print(a.get('377774355'))


