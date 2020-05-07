import json

def print_list(a):
	r = ''
	for i in a:
		r = r + '[\''+i+'\': '+'\''+a[i]+'\']\n'
	return r

def readlist(filename):
	with open(filename, 'r') as f:  
		list = json.load(f)
	return list

def writelist(filename, list):
	with open(filename, 'w') as f:  
		json.dump(list, f)

try:
	readlist('rights.txt')
except:
	writelist('rights.txt', {})

n = None
while (n != 's') and (n != 'save') and (n != '^S'):
	d = readlist('rights.txt')
	print(print_list(d))
	n = input('/')
	if n == 'add':
		id = input('Add ID:')
		role = input('Add role:')
		d.update({id:role})
		writelist('rights.txt', d)
	elif n == 'remove':
		id = input('Remove ID:')
		d.pop(id, None)
		writelist('rights.txt', d)
	else:
		print('Команды:\n-save\n-s\n-add \n-remove\n')

