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

def try_int(a, Except=None):
	try:
		a = int(a)
	except:
		a = Except
	return a

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
		f.close()
		if balance == '':
			try:
				f = open('balances/'+str(id), 'w+')
				f.write('0')
				f = open('balances/'+str(id), 'r+')
				balance = clean(f.read())
			except:
				None
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
		'''
		try:
			int(balance)
		except:
			f = open('balances/'+str(id), 'w+')
			f.write('0')
			f = open('balances/'+str(id), 'r+')
			balance = clean(f.read())
		'''
		return int(clean(balance))

def transfer(from_id, to_id, amount, reply_id=None):
	if reply_id == None:
		reply_id = from_id
	if (int(amount) <= 0) and (rights(from_id) != 'admin'):
		write_msg(from_id, 'Сумма должна быть больше 0\nБаланс: '+str(balance(from_id))+" Work Coins")
		rp = 'lt0'
	elif rights(from_id) != 'admin':
		if balance(from_id) >= int(amount):
			fb = int(balance(from_id))
			tb = int(balance(to_id))
			f = open('balances/'+str(from_id), 'w+')
			f.write(str(int(fb-int(amount))))
			f.close()
			balance(to_id)
			f = open('balances/'+str(to_id), 'w+')
			f.write(str(int(tb+int(amount))))
			f.close()
			write_msg(reply_id, "\U0001F4E4 Вы заплатили "+str(amount)+" Work Coins\n\U0001F3AF Получатель: "+str(name(to_id))+"\n\U0001F4B3 Ваш баланс: "+str(balance(from_id))+" Work Coins")
			write_msg(to_id, "\U0001F4E5 Вам пришшло "+str(amount)+" Work Coins\n\U0000270F Отправитель: "+name(from_id)+"\n\U0001F4B3 Ваш бпланс: "+str(balance(to_id))+" Work Coins")
			rp = 'successfull'
		else:
			write_msg(from_id, 'Не хватает средств\nБаланс: '+str(balance(from_id))+" Work Coins")
			rp = 'amount'
	elif rights(from_id) == 'admin':
		tb = int(balance(to_id))
		balance(to_id)
		f = open('balances/'+str(to_id), 'w+')
		f.write(str(int(tb+int(amount))))
		f.close()
		write_msg(reply_id, "\U0001F4E4 Вы заплатили "+str(amount)+" Work Coins\n\U0001F3AF Получатель: "+str(name(to_id)))
		write_msg(to_id, "\U0001F4E5 Вам пришшло "+str(amount)+" Work Coins\n\U0000270F Отправитель: "+name(from_id)+"\n\U0001F4B3 Ваш бпланс: "+str(balance(to_id))+" Work Coins")
		rp = 'successfull'


def ru_rights(id):
	if rights(id)=='admin':
		r = 'Админ'
	elif rights(id)=='sysadmin':
		r = 'Сисадмин'
	elif rights(id)=='member':
		r = 'Участник'
	return r

def stats(id):
	if rights(id) != 'admin':
		write_msg(id, 'Вы\U0001F464\n\U0001F3F7 Имя: '+name(id)+'\n\U0001F194 ID: [https://vk.com/id'+str(id)+'|'+str(id)+']\n\U0001F510 Статус: '+ru_rights(id)+'\n\U0001F4B3 Баланс: '+str(balance(id))+' WorkCoins')
	else:
		write_msg(id, 'Вы\U0001F464\n\U0001F3F7 Имя: '+name(id)+'\n\U0001F194 ID: [https://vk.com/id'+str(id)+'|'+str(id)+']\n\U0001F510 Статус: '+ru_rights(id))



def send_list(id, send=None, id2=None):
	k = ''
	n = 0
	if send == None:
		for i in members():
			if str(i) != str(id):
				n = n + 1
				k = k + str(n)+'. '+name(i)+' ('+ru_rights(i)+')'+'\n'
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

def try_path(id, n, Except=None):
	try:
		r = path[id][n]
	except:
		r = Except
	return r

#def path(path):



#########################

try: readlist('rights.txt')
except: writelist('rights.txt',{})

path = {}


# API-ключ созданный ранее
token = "75dd5c9e66affd3016d6156516e8a4bd6fe62e51e40adae1ff6dcd02b002a2da2ab0ee4e73465f582fea1"

# Авторизуемся как сообщество
vk = vk_api.VkApi(token=token)

# Работа с сообщениями
longpoll = VkLongPoll(vk)

# Commander
commander = Commander()

print("Бот запущен")
while True:
	try:
# Основной цикл
		for event in longpoll.listen():

		    # Если пришло новое сообщение
			if event.type == VkEventType.MESSAGE_NEW:

		        # Если оно имеет метку для меня( то есть бота)
				if event.to_me:

		            # Сообщение от пользователя
					request = event.text

        		    # Путь
					path.setdefault(event.user_id, ['home'])

		            # Каменная логика ответа

##############################################################################################
#                                  УСЛОВИЯ БЕЗ УЧЕТА ПУТИ                                    #
##############################################################################################


					if clean(request) == "id":
						write_msg(event.user_id,'\U0001F194 Ваш ID:')
						write_msg(event.user_id, event.user_id)


					elif clean(request) == 'я':
						if str(event.user_id) in members():
							stats(event.user_id)
						else:
							write_msg(event.user_id, deny())


					elif clean(request) == 'баланс':
						if str(event.user_id) in members():
							if (rights(event.user_id) == 'member') or (rights(event.user_id) == 'sysadmin'):
								write_msg(event.user_id, '\U0001F4B3 Баланс: '+str(balance(event.user_id))+' WorkCoin')
							else:
								write_msg(event.user_id, deny())
						else:
							write_msg(event.user_id, deny())

					elif clean(request) == 'path':
						if str(event.user_id) in members():
							write_msg(event.user_id, str(path[event.user_id]))
						else:
							write_msg(event.user_id, deny())


#############################################################################################
#                                   УСЛОВИЯ С УЧЕТОМ ПУТИ                                   #
#############################################################################################
# 		            H O M E // P A Y // I D // < I D > // A M O U N T
					elif (try_path(event.user_id,0) == 'home') and (try_path(event.user_id,1) == 'pay') and (try_path(event.user_id,2) == 'id') and (try_path(event.user_id,4) == 'amount') and (len(path[event.user_id]) == 5):
						if try_int(request) != None:
							if transfer(event.user_id, path[event.user_id][3], request) == 'successfull':
								path[event.user_id] = ['home']
						elif (clean(request) == 'помощь') or (clean(request) == 'помощь'):
							write_msg(event.user_id, '\U00002757 Укажите количество WorkCoins, которое нужно перевести '+name(path[event.user_id][3])+' или напишите "Отмена"')
						elif clean(request) == 'отмена':
							path[event.user_id] = ['home']
							write_msg(event.user_id, 'Платеж отменен \U0000274C')
						else:
							write_msg(event.user_id, '\U000026A0 Вы что-то написали не так\n\n\U00002757 Укажите количество WorkCoins, которое нужно перевести или напишите "Отмена"')
#		            H O M E // P A Y // I D
					elif (path[event.user_id] == ['home','pay','id']):
						try:
							nm = str(name(clean(request)))
						except:
							nm = None
						if nm != None:
							write_msg(event.user_id, '\U00002753 Сколько WorkCoins перевести '+nm+'?')
							path[event.user_id] = ['home','pay','id',clean(request),'amount']

						elif clean(request) == 'отмена':
							path[event.user_id] = ['home']
							write_msg(event.user_id, 'Платеж отменен \U0000274C')

						elif (clean(request) == 'помощь') or (clean(request) == 'помощь'):
							write_msg(event.user_id, '\U00002757 Введите ID получателя или используйте команду "Отмена"')

						else:
							write_msg(event.user_id, '\U000026A0 Не существующий ID')

#                   H O M E // P A Y // L I S T
					elif (path[event.user_id] == ['home','pay','list']):
						if send_list(event.user_id, send=True, id2=try_int(request)) != None:
							write_msg(event.user_id, 'Сколько WorkCoins перевести '+name(send_list(event.user_id, send=True, id2=try_int(request)))+'?')
							path[event.user_id] = ['home','pay','id',send_list(event.user_id, send=True, id2=try_int(request)),'amount']

						elif clean(request) == 'отмена':
							path[event.user_id] = ['home']
							write_msg(event.user_id, 'Платеж отменен \U0000274C')

						elif (clean(request) == 'помощь') or (clean(request) == 'помощь'):
							write_msg(event.user_id, '\U00002757 Выберите игрока из списка:\n'+send_list(event.user_id)+'\n\n\U0001F4CC Или используйте команду "Отмена"')

						else:
							write_msg(event.user_id, '\U000026A0 Не существующий номер')



#                   H O M E // P A Y

					elif (path[event.user_id] == ['home','pay']) :
						if ((clean(request) == 'команды') or (clean(request) == 'помощь')):
							if str(event.user_id) in members():
								write_msg(event.user_id, '\U00002757 Выберите номер способа отправки или отмену из списка\n\n\U00002709 Список:\n1. Игрок из списка\n2. ID\n3. Отмена')

							else:write_msg(event.user_id, deny())


						else:
							if str(event.user_id) in members():
									if clean(request) == '1':
										write_msg(event.user_id, '\U0001F3AF Выберите игрока из списка:\n'+send_list(event.user_id))
										path[event.user_id] = ['home','pay','list']
									elif clean(request) == '2':
										write_msg(event.user_id, '\U0001F194 Введите ID получателя')
										path[event.user_id] = ['home','pay','id']
									elif (clean(request) == '3') or (clean(request) == 'отмена'):
										write_msg(event.user_id, 'Платеж отменен \U0000274C')
										path[event.user_id] = ['home']
									else: 
										write_msg(event.user_id, '\U000026A0 Такой команды нет\n\n\U00002757 Чтобы узнать доступные команды напишите "Команды"')
							else:write_msg(event.user_id, deny())
				

					#elif path[event.user_id]



#                   H O M E

					elif path[event.user_id] == ['home'] and ((clean(request) == 'отправить') or (clean(request) == 'заплатить') or (clean(request) == 'перевести')):
						if str(event.user_id) in members():
							path[event.user_id] = ['home','pay']
							write_msg(event.user_id, '\U00002709 Выберите способ отправки:\n\n1. Игрок из списка\n2. ID\n3. Отмена')

						else:
							write_msg(event.user_id, deny())


					elif (clean(request) == 'команды') or (clean(request) == 'помощь'):
						if str(event.user_id) in members():
							if (rights(event.user_id) == 'member') or (rights(event.user_id) == 'sysadmin'):
								write_msg(event.user_id, '\U0001F4C3 Список команд:\n • Я\n • Баланс\n • id\n • Команды\n • Отправить')

							elif rights(event.user_id) == 'admin':
								write_msg(event.user_id, '\U0001F4C3 Список команд:\n • Я\n • id\n • Команды\n • Отправить')

							else:
								write_msg(event.user_id, deny())
						else:
							write_msg(event.user_id, deny())


					else:
						write_msg(event.user_id,'\U000026A0 Такой команды нет.\n\n\U00002757 Чтобы узнать доступные номанды напишите "Команды"')

	except requests.exceptions.ReadTimeout:
		print('ERROR: Requests "ReadTimeout"')

