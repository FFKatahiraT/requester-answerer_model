import socket
import time        

def connect():
	global connected
	# Привязываемся к порту
	try:
		s.connect(('127.0.0.1', port))
		connected = True
		print('В СЕТИ')
	except:
		connected = False
		print('КАНАЛ СВЯЗИ НЕДОСТУПЕН')

def send_code():	#Отправляем код
	if connected == True:	#Если подключение есть
		s.send('1'.encode())	#отправляем еденицу
		for tau in answer_codes[code_index]:
			time.sleep(tau*0.1)	#ms*100	Если нужное кол-во времени прошло 
			s.send('1'.encode())	#отправляем еденицу
		print('Сообщение отправлено')
	else:
		print('Канал связи отключен')
		print('Связываюсь с сервером')
		connect()	

def find_code(recv_time):	#Находим индекс кода более похожего на определенный код запроса
	subtraction = []
	for i in range(len(recv_time)):
		subtraction.append(0)
		for k in range(len(request_codes[i])):
			print(subtraction[i], 'subtraction[i]')
			subtraction[i] += request_codes[i][k]*0.1-recv_time[k]
	print(recv_time, 'Время прихода сообщений')
	return subtraction.index(min(subtraction))

s = socket.socket()
# Привязываемся к порту
port = 8936           
connect()

request_codes = [[4,6], [4,7], [3,6], [3,7]]	#Коды запросов
answer_codes = [[10,10,10],[4,7,15],[3,6,10],[3,7,15]]	#Коды ответов
code_index = 0	#Текущий код

# Получаем данные с сервера и декодируем их
data, recv_time = [], []
while s:
	data.append(s.recv(1024).decode())
	if len(data) == 1:
		start_time = time.time()
	else:
		recv_time.append(time.time() - start_time)
	if len(data)>=3:
		code_index = find_code(recv_time)
		send_code()
		data, recv_time = [], []