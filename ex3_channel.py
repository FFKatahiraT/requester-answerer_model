import select
import socket
import sys
import queue
import time

distance = 1500 #km
speed = 3*10**3	#m/s 
wait_time = distance*10**3/speed
print(wait_time, 'wait_time')

c, addr = [], []

server = socket.socket()		
print ("Сокет успешно создан")
 
# Привязываемся к порту
port = 8936		   
server.bind(('127.0.0.1', port))	#Поле ip может быть пустым	
print ("Сокет привязан к порту %s" %(port))
 
# Переводим сокет в режим прослушки
server.listen(5)	
print ("Сокет в режиме прослушки")		   

# Sockets from which we expect to read
inputs = [server]
# Sockets to which we expect to write
outputs = []
# Outgoing message queues (socket:Queue)
message_queues = {}
while inputs:
	# Wait for at least one of the sockets to be ready for processing
	readable, writable, exceptional = select.select(inputs, outputs, inputs)
	# print(len(readable), 'readable')
	# print(len(writable), 'writable')
	# print(len(exceptional), 'exceptional')
	 # Handle inputs
	for s in readable:
		if s is server:
			# A "readable" server socket is ready to accept a connection
			connection, client_address = s.accept()
			print('Клиент подключен: ', client_address)
			connection.setblocking(0)
			inputs.append(connection)
			# Give the connection a queue for data we want to send
			message_queues[connection] = queue.Queue()
		else:
			data = s.recv(1024).decode()
			if data:
				# A readable client socket has data
				print('Получено "%s" от %s' % (data, s.getpeername()))
				# Добавляем канал в получатели ответа
				for receiver in inputs:
					if receiver != s and receiver not in outputs and receiver != server:	#Кроме исходящего канала, сервера
						message_queues[receiver].put(data)
						outputs.append(receiver)
			else:
				# Interpret empty result as closed connection
				# print('closing', client_address, 'after reading no data')
				# Stop listening for input on the connection
				if s in outputs:
					outputs.remove(s)
				inputs.remove(s)
				s.close()
				# Remove message queue
				del message_queues[s]
	 # Handle outputs
	for s in writable:
		try:
			message = message_queues[s].get_nowait()
		except queue.Empty:
			# No messages waiting so stop checking for writability.
			# print('output queue for', s.getpeername(), 'is empty')
			outputs.remove(s)
		else:
			time.sleep(wait_time)
			print('"%s" Отправлено %s' % (message, s.getpeername()))
			s.send(message.encode())
	 # Handle "exceptional conditions"
	for s in exceptional:
		print('handling exceptional condition for', s.getpeername())
		# Stop listening for input on the connection
		inputs.remove(s)
		if s in outputs:
			outputs.remove(s)
		s.close()
		# Remove message queue
		del message_queues[s]



# while True:
# 	# Устанавливаем соединение с клиентом
# 	c_temp, addr_temp = s.accept()
# 	c.append(c_temp)
# 	addr.append(addr_temp)
# 	print ('получено соединение от', addr )

# 	# Отправляем клиенту сообщение. кодируем для отправки байтового типа.
# 	c.send('Thank you for connecting'.encode())

# 	c.close()
# 	break