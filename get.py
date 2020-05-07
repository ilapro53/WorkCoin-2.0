import vk_api
import random
from vk_api.longpoll import VkLongPoll, VkEventType

from commander.commander import Commander

def get_random_id():
    return random.getrandbits(31) * random.choice([-1, 1])

def write_msg(user_id, message):
    vk.method('messages.send', {'user_id': user_id, 'message': message, "random_id":get_random_id()})



# API-ключ созданный ранее
token = "572f542d96f5ed6540f98f13010d3026ef0716660711e4e1ae3f79a778d45e434169b95bb3ed95f17fc98"

# Авторизуемся как сообщество
vk = vk_api.VkApi(token=token)

# Работа с сообщениями
longpoll = VkLongPoll(vk)

# Commander
commander = Commander()

print("Бот запущен")
# Основной цикл
for event in longpoll.listen():

	# Если пришло новое сообщение
	if event.type == VkEventType.MESSAGE_NEW:
		
		# Если оно имеет метку для меня( то есть бота)
		if event.to_me:

			# Сообщение от пользователя
			request = event.text

			# Каменная логика ответа
			write_msg(event.user_id, request)
			print(request)
			request=int(request)
			if isinstance(request, int):
			 print('int')

