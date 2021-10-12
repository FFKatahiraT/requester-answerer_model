import random
import pygame
import time

class requester:
	def __init__(self):
		self.msg_sent_tics = 0
		self.code_index = 0

	def send(self):
		self.msg_sent_tics = time.time()	#Отсчитываем время от отправления запроса
		send_code(answerer1, request_codes[self.code_index])
		# msg.append('Сообщение отправлено')
		
	def recv(self, function_t):
		global msg
		recv_time = []
		for s in range(1, len(function_t)):	#Превращаем сигнал в данные
			if function_t[s] == 1:
				recv_time.append(function_t[s])	#Добавляем промежутки между сигналами [ms]
		# print(time.time(),'time.time()')
		time_measured = time.time() - self.msg_sent_tics	#Расчитываем время с учетом приема сообщения ответчиком, разницей длины сообщений ответчика и запросчика, а также погрешности программы
		distance = speed_of_light*time_measured/10**3 - 20	#km
		msg.append('ДИСТАНЦИЯ ДО ОБЪЕКТА: '+str(round(distance/2,2))+' km')
		msg.append('Время ожидания: ' + str(round(time_measured*10**6,2)) + ' us')
		self.data, self.recv_time = [], []
		self.start_time = 0

class answerer:
	def recv(self, function_t):
		recv_time = []
		for s in range(1, len(function_t)):	#Превращаем сигнал в данные
			if function_t[s] == 1:
				recv_time.append(s)	#Добавляем промежутки между сигналами [ms]
		code_index = find_code(recv_time, request_codes)
		send_code(requester1, answer_codes[code_index])
		recv_time = []
	
class channel:
	def __init__(self, distance):
		self.wait_time = distance*10**3/speed_of_light	#s
		print(self.wait_time, 'wait_time')

	def start(self, receiver, function_t):
		time.sleep(self.wait_time)
		receiver.recv(function_t)

def find_code(recv_time, sender_codes):	#Находим индекс кода более похожего на определенный код запроса
	subtraction = []
	for i in range(len(sender_codes)):
		subtraction.append(0)
		for k in range(len(recv_time)):
			subtraction[i] += abs(sender_codes[i][k]-recv_time[k])	#ms
	index = subtraction.index(min(subtraction))
	print('Ответчик:', recv_time, 'recv_time')
	print('Ответчик:', index+1, 'Код запроса')
	return index

def send_code(receiver, codes):	#Отправляем код
	global msg
	function_t = []	#Функция сигнала (t) [ms]
	for t in range(max(codes)+1):	#Заполняем функцию сигналом
		if t in codes or t == 0:
			function_t.append(1)
		else:
			function_t.append(0)
	print(function_t, 'function_t')
	channel1.start(receiver, function_t)	#отправляем функцию (последовательность)

def increase_tau(request_codes):
	for i in range(len(request_codes)):
		for k in range(len(request_codes[i])):
			request_codes[i][k]*=1
	return request_codes

def decrease_code_index(code_index):	#Изменяем выбранный код ЗС
	if code_index <= 0:
		code_index = len(request_codes)-1
	else:
		code_index -= 1
	return code_index

def increase_code_index(code_index):	#Изменяем выбранный код ЗС
	if code_index >= len(request_codes)-1:
		code_index = 0
	else:
		code_index += 1
	return code_index

#######################FRONTEND_FUNCTIONS_BELOW#######################
def button_hovered(button_xy, textsurface):
	button_xy_centered=[]
	for i in range(len(button_xy)):
		button_xy_centered.append(button_xy[i]-button_size[i]//2)
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
		gameDisplay.blit(msg_ts, (display_width//2, int(display_heigth*(0.05+i*0.1))))

pygame.init()	#Запускаем pygame
pygame.font.init()
textfont = pygame.font.SysFont('Comic Sans MS', 30)	#инициализируем шрифт

display_width = int(1280*0.5)
display_heigth = int(720*0.5)
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

button_send_xy = [int(display_width*0.2),int(display_heigth*0.2)]
button_left_xy = [int(display_width*0.1),int(display_heigth*0.5)]
button_right_xy = [int(display_width*0.3),int(display_heigth*0.5)]
button_random_code_xy = [int(display_width*0.2),int(display_heigth*0.7)]
button_quit_xy = [int(display_width*0.2),int(display_heigth*0.9)]

send_ts = textfont.render('ОТПРАВИТЬ', False, light_yellow)
choose_code_ts = textfont.render('КОД ЗС', False, light_yellow)
dec_code_ts = textfont.render('<-', False, light_yellow)
inc_code_ts = textfont.render('->', False, light_yellow)
random_code_ts = textfont.render('СЛУЧАЙНЫЙ КОД', False, light_yellow)
quit_ts = textfont.render('ВЫХОД', False, light_yellow)

choose_code_ts_xy = (int(display_width*0.14), int(display_heigth*0.35))
code_index_ts_xy = (int(display_width*0.2), int(display_heigth*0.46))
##############Инициализация переменных##############
speed_of_light = 3*10**8	#m/s скорость сигнала
request_codes = [[4,6], [4,7], [3,6], [3,7]]	#Коды запросов ms
answer_codes = [[4,6,10],[4,7,15],[3,6,10],[3,7,15]]	#Коды ответов ms
request_codes = increase_tau(request_codes)	#увеличиваем интервал между сигналами
answer_codes = increase_tau(answer_codes)

distance = 150
####################################################
channel1 = channel(distance)	#Агрумент -- расстояние в км
requester1 = requester() #Создаем объекты
answerer1 = answerer()

msg = []	#Сообщения от программы
FPS = 60
running = True
while running:
	mouse = pygame.mouse.get_pos()	#получаем местоположение мыши
	for event in pygame.event.get():
		if event.type == pygame.QUIT:	#выход из программы
			running = False
		if event.type == pygame.MOUSEBUTTONDOWN:
			if -button_size[0]/2<=mouse[0]-button_send_xy[0]<=button_size[0]/2 and -button_size[1]/2<=mouse[1]-button_send_xy[1]<=button_size[1]/2:
				requester1.send()	#Отправляем запрос
			elif -button_size[0]/2<=mouse[0]-button_left_xy[0]<=button_size[0]/2 and -button_size[1]/2<=mouse[1]-button_left_xy[1]<=button_size[1]/2:
				requester1.code_index = decrease_code_index(requester1.code_index)
			elif -button_size[0]/2<=mouse[0]-button_right_xy[0]<=button_size[0]/2 and -button_size[1]/2<=mouse[1]-button_right_xy[1]<=button_size[1]/2:
				requester1.code_index = increase_code_index(requester1.code_index)
			elif -button_size[0]/2<=mouse[0]-button_random_code_xy[0]<=button_size[0]/2 and -button_size[1]/2<=mouse[1]-button_random_code_xy[1]<=button_size[1]/2:
				requester1.code_index = random.randint(0, len(request_codes)-1)
			elif -button_size[0]/2<=mouse[0]-button_quit_xy[0]<=button_size[0]/2 and -button_size[1]/2<=mouse[1]-button_quit_xy[1]<=button_size[1]/2:
				running = False
	if len(msg) >= 6:	#Удаляем старые сообщения
		msg = msg[1:]
	code_index_ts = textfont.render(str(requester1.code_index+1), False, light_yellow)	#рендерим текущее значение кода ЗС
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