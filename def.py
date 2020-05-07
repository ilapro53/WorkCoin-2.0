import vk_api
import random
import json
from vk_api.longpoll import VkLongPoll, VkEventType

from commander.commander import Commander

def get_random_id():
    return random.getrandbits(31) * random.choice([-1, 1])

def write_msg(user_id, message):

    vk.method('messages.send', {'user_id': user_id, 'message': message, "random_id":get_random_id()})



######## ФУНКЦИИ ########
def readlist(filename):
	with open(filename, 'r') as f:  
		list = json.load(f)
	return list

def writelist(filename, list):
	with open(filename, 'w') as f:  
		json.dump(list, f)

# # # # # # # # # # # # #
def clean(request):
	request = request.replace('.','')
	request = request.lower().strip()
	request2 = request
	request = request.replace("  ", " ")
	while request2 != request:
		request2 = request
		request = request.replace("  ", " ")
	return request


def rights(id):
	list = readlist('rights.txt')
	rights = list.get(str(id))
	return rights

def removemember(id):
	return a.pop(id, None)

def members():
	return list(readlist('rights.txt').keys())

def deny():
	return '\U000026D4Отказано в доступе\U000026D4'

def name(id):
	user = vk.method("users.get", {"user_ids": id})
	fullname = user[0]['first_name'] +  ' ' + user[0]['last_name']
	return fullname

def balance(id):
	id = str(id)
	try:
		f = open('balances/'+str(id), 'r+')
		balance = clean(f.read())
	except:
		f = open('balances/'+str(id), 'w+')
		f.write('0')
		f = open('balances/'+str(id), 'r+')
		balance = clean(f.read())
	finally:
		try:
			f.close()
		except:
			None
		return int(balance)

def transfer(from_id, to_id, amount, reply_id=None):
	if reply_id == None:
		reply_id = from_id
	if balance(from_id) >= amount:
		f = open('balances/'+str(from_id), 'w+')
		f.write(clean(str(balance(from_id)-amount)))
		f.close()
		balance(to_id)
		f = open('balances/'+str(to_id), 'w+')
		f.write(clean(str(balance(to_id)+amount)))
		f.close()
		write_msg(reply_id, "\U0001F4E4 Вы заплатили "+str(amount)+" Work Coins\n Получатель: "+str(name(to_id))+"\n\U0001F4B3 Ваш баланс: "+str(balance(from_id))+" Work Coins")
		write_msg(to_id, "Вам пришшло "+str(amount)+" Work Coins\nОтправитель: "+name(from_id)+"\n\U0001F4B3 Ваш бпланс: "+str(balance(to_id))+" Work Coins")



def ru_rights(id):
	if rights(id)=='admin':
		r = 'Админ'
	elif rights(id)=='sysadmin':
		r = 'Сисадмин'
	elif rights(id)=='member':
		r = 'Участник'
	return r

def stats(id):
	write_msg(id, 'Вы\U0001F464\n\U0001F3F7 Имя: '+name(id)+'\n\U0001F194 ID: [https://vk.com/id'+str(id)+'|'+str(id)+']\n\U0001F510 Статус: '+ru_rights(id)+'\n\U0001F4B0 Баланс: '+str(balance(id))+' WorkCoin')

def try_int(a, Except=None):
	try:
		a = int(a)
	except:
		a = Except
	return a

def send_list(id, send=None, id2=None):
	k = ''
	n = 0
	if send == None:
		for i in members():
			if str(i) != str(id):
				n = n + 1
				k = k + str(n)+'. '+name(i)+'\n'
	elif send == True:
		k = None
		for i in members():
			if str(i) != str(id):
				n = n + 1
				if str(n) == str(id2):
					k = i
	elif send == 'max':
		for i in members():
			if str(i) != str(id):
				n = n + 1
				k = n
	return k


token = "75dd5c9e66affd3016d6156516e8a4bd6fe62e51e40adae1ff6dcd02b002a2da2ab0ee4e73465f582fea1"

# Авторизуемся как сообщество
vk = vk_api.VkApi(token=token)

# Работа с сообщениями
longpoll = VkLongPoll(vk)

# Commander
commander = Commander()

print(send_list(id, send=True, id2=2))