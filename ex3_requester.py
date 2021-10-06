import socket
import random
import pygame
import select

def connect():
	global connected, msg
	# Привязываемся к порту
	try:
		s.connect(('127.0.0.1', port))
		connected = True
		msg.append('В СЕТИ')
	except:
		connected = False
		msg.append('КАНАЛ СВЯЗИ НЕДОСТУПЕН')

def button_hovered(button_xy, textsurface):
	button_xy_centered=[]
	for i in range(len(button_xy)):
		button_xy_centered.append(button_xy[i]-button_size[i]/2)
	mouse = pygame.mouse.get_pos()
	if 0<=mouse[0]-button_xy_centered[0]<=button_size[0] and 0<=mouse[1]-button_xy_centered[1]<=button_size[1]:
		pygame.draw.rect(gameDisplay,green,button_xy_centered+button_size)
	else:
		pygame.draw.rect(gameDisplay,dark_green,button_xy_centered+button_size)	
	gameDisplay.blit(textsurface, button_xy_centered)

def button_hovered_circle(button_xy, textsurface):
	for i in range(len(button_xy)):
		button_xy[i] = int(button_xy[i])
	mouse = pygame.mouse.get_pos()
	if -button_size_circle[0]/2<=mouse[0]-button_xy[0]<=button_size_circle[0]/2 and -button_size_circle[1]/2<=mouse[1]-button_xy[1]<=button_size_circle[1]/2:
		pygame.draw.circle(gameDisplay,green,button_xy, button_size_circle[0]//2)	
	else:
		pygame.draw.circle(gameDisplay,dark_green,button_xy, button_size_circle[0]//2)	
	gameDisplay.blit(textsurface, (button_xy[0]-button_size_circle[0]//5, button_xy[1]-button_size_circle[0]//5))

def send_code():	#Отправляем код
	global msg
	if connected == True:	#Если подключение есть
		start_ticks=pygame.time.get_ticks()	#Запускаем таймер
		s.send('1'.encode())	#отправляем еденицу
		i = 0
		while i < len(codes[code_index]):
			if pygame.time.get_ticks() - start_ticks >= codes[code_index][i]*100:	#Если нужное кол-во времени прошло 
				s.send('1'.encode())	#отправляем еденицу
				start_ticks=pygame.time.get_ticks()	#И запускаем таймер снова
				i+=1
		msg.append('Сообщение отправлено')
		msg_sent_tics = pygame.time.get_ticks()	#Отсчитываем время от отправления запроса
		recv_code(msg_sent_tics)
	else:
		msg.append('Канал связи отключен')
		msg.append('Связываюсь с сервером')
		connect()	

def recv_code(msg_sent_tics):
	global msg
	data = []
	while len(data) < 4:
		ready = select.select([s], [], [], 5)	#Если пройдет более 5 секунд, ожидание сообщение будет прекращено
		if ready[0]:
			data.append(s.recv(1024).decode())
		else:
			msg.append('Время ожидания ответа истекло')
			break
	else:
		time_measured = pygame.time.get_ticks() - msg_sent_tics
		distance = speed*time_measured	#km
		msg.append('ДИСТАНЦИЯ ДО ОБЪЕКТА: '+str(distance)+' km')
		msg.append('Время ожидания: ' + str(round(time_measured/1000),2) + ' s')


def decrease_code_index(code_index):	#Изменяем выбранный код ЗС
	if code_index <= 0:
		code_index = len(codes)-1
	else:
		code_index -= 1
	return code_index

def increase_code_index(code_index):	#Изменяем выбранный код ЗС
	if code_index >= len(codes)-1:
		code_index = 0
	else:
		code_index += 1
	return code_index

def blit_msg(msg):
	line_msg = []
	words_in_line = 22
	for messages in msg:
		while len(messages)>words_in_line:
			line_msg.append(messages[:words_in_line])
			messages = messages[words_in_line:]
		line_msg.append(messages)
	for i in range(len(line_msg)):
		msg_ts = textfont.render(line_msg[i], False, light_yellow)	#рендерим сообщения от программы
		gameDisplay.blit(msg_ts, (int(display_width*0.5), int(display_heigth*(0.05+i*0.1))))


s = socket.socket()	#Создаем сокет
port = 8936
connected = False
s.setblocking(0)

pygame.init()	#Запускаем pygame
pygame.font.init()
textfont = pygame.font.SysFont('Comic Sans MS', 30)	#инициализируем шрифт

display_width = int(1280/2)
display_heigth = int(720/2)
gameDisplay = pygame.display.set_mode((display_width, display_heigth))	#Инициализируем экран

pygame.display.set_caption('Запросчик')	#Добавляем название
clock = pygame.time.Clock()	#И время

black = (0,0,0)	#Задаем цвета
light_yellow = (250,240,173)
dark_green = (80, 120, 0)
red = (255, 0, 0)
green = (120, 160, 0)
blue = (0, 0, 255)
dark_slate_gray = (47,79,79)

##############Задаем кнопки##############
button_size = [200, 50]
button_size_circle = [50, 50]

button_send_xy = [display_width*0.2,display_heigth*0.2]
button_left_xy = [display_width*0.1,display_heigth*0.5]
button_right_xy = [display_width*0.3,display_heigth*0.5]
button_random_code_xy = [display_width*0.2,display_heigth*0.7]
button_quit_xy = [display_width*0.2,display_heigth*0.9]

send_ts = textfont.render('ОТПРАВИТЬ', False, light_yellow)
choose_code_ts = textfont.render('КОД ЗС', False, light_yellow)
dec_code_ts = textfont.render('<-', False, light_yellow)
inc_code_ts = textfont.render('->', False, light_yellow)
random_code_ts = textfont.render('СЛУЧАЙНЫЙ КОД', False, light_yellow)
quit_ts = textfont.render('ВЫХОД', False, light_yellow)

choose_code_ts_xy = (display_width*0.14, display_heigth*0.35)
code_index_ts_xy = (display_width*0.2, display_heigth*0.46)
##########################################

codes = [[4,6], [4,7], [3,6], [3,7]]	#Коды запросов
code_index = 0	#Текущий код
speed = 3*10**3	#m/s скорость сигнала
msg = []	#Сообщения от программы

connect()
FPS = 60
running = True
while running:
	mouse = pygame.mouse.get_pos()	#получаем местоположение мыши
	for event in pygame.event.get():
		if event.type == pygame.QUIT:	#выход из программы
			running = False
		if event.type == pygame.MOUSEBUTTONDOWN:
			if -button_size[0]/2<=mouse[0]-button_send_xy[0]<=button_size[0]/2 and -button_size[1]/2<=mouse[1]-button_send_xy[1]<=button_size[1]/2:
				send_code()	#Отправляем запрос
			elif -button_size[0]/2<=mouse[0]-button_left_xy[0]<=button_size[0]/2 and -button_size[1]/2<=mouse[1]-button_left_xy[1]<=button_size[1]/2:
				code_index = decrease_code_index(code_index)
			elif -button_size[0]/2<=mouse[0]-button_right_xy[0]<=button_size[0]/2 and -button_size[1]/2<=mouse[1]-button_right_xy[1]<=button_size[1]/2:
				code_index = increase_code_index(code_index)
			elif -button_size[0]/2<=mouse[0]-button_random_code_xy[0]<=button_size[0]/2 and -button_size[1]/2<=mouse[1]-button_random_code_xy[1]<=button_size[1]/2:
				code_index = random.randint(0, len(codes)-1)
			elif -button_size[0]/2<=mouse[0]-button_quit_xy[0]<=button_size[0]/2 and -button_size[1]/2<=mouse[1]-button_quit_xy[1]<=button_size[1]/2:
				running = False
	if len(msg) >= 7:	#Удаляем старые сообщения
		msg = msg[1:]
	code_index_ts = textfont.render(str(code_index+1), False, light_yellow)	#рендерим текущее значение кода ЗС
	#Выводим на экран надписи и кнопки
	gameDisplay.fill(dark_slate_gray)
	blit_msg(msg)
	gameDisplay.blit(choose_code_ts, choose_code_ts_xy)
	gameDisplay.blit(code_index_ts, code_index_ts_xy)
	button_hovered(button_send_xy,send_ts)
	button_hovered_circle(button_left_xy,dec_code_ts)
	button_hovered_circle(button_right_xy,inc_code_ts)
	button_hovered(button_random_code_xy,random_code_ts)
	button_hovered(button_quit_xy, quit_ts)
	pygame.display.update()	#обновляем экран
	clock.tick(FPS)



# # Получаем данные с сервера и декодируем их
# print (s.recv(1024).decode())
# s.close()