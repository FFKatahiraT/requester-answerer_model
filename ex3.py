import random
import pygame
import time
from multiprocessing import Pool

class requester:
	def __init__(self, code_index):
		self.signal_noise_norm_distr = []	#Задаем распределение сигнала, он будет пополняться по ходу работы
		self.msg_sent_tics = 0
		self.code_index = code_index
		self.False_signals = 0
		self.target_loss = 0
		self.distance = 0
		self.time_measured = 0

	def send(self):
		self.msg_sent_tics = time.time()	#Отсчитываем время от отправления запроса
		send_code(answerer1, request_codes[self.code_index])
		# msg.append('Сообщение отправлено')
		
	def recv(self, function_t):
		global msg
		processing_start_time = time.time()
		print(function_t, ' Получено запросчиком')
		recv_time = []
		self.signal_noise_norm_distr, exp_val = find_expected_value(self.signal_noise_norm_distr, function_t)
		print(noise_exp_value/exp_val*max(function_t), ' Порог запросчика\n')
		for s in range(1, len(function_t)):	#Превращаем сигнал в данные
			if function_t[s] >= noise_exp_value/exp_val*max(function_t):
				recv_time.append(s)	#Добавляем промежутки между сигналами [ms]
		# print(time.time(),'time.time()')
		self.False_signals, self.target_loss = error_analyzer(answer_codes[self.code_index], recv_time)	#Анализируем ошибки
		processing_time = time.time() - processing_start_time	#Время обработки сигнала
		self.time_measured = time.time() - self.msg_sent_tics - processing_time*2	#Расчитываем время с учетом приема сообщения ответчиком, разницей длины сообщений ответчика и запросчика, а также погрешности программы
		self.distance = (speed_of_light*self.time_measured/10**3 - 20)/2	#km
		self.data, self.recv_time = [], []
		self.start_time = 0

class answerer:
	def __init__(self):
		self.signal_noise_norm_distr = []	#Задаем распределение сигнала, он будет пополняться по ходу работы

	def recv(self, function_t):
		print(function_t, ' Получено ответчиком')
		recv_time, true_signal_candidate = [], []
		self.signal_noise_norm_distr, exp_val = find_expected_value(self.signal_noise_norm_distr, function_t)	#ищем мат ожидание
		# print(noise_exp_value/exp_val*max(function_t), ' Порог ответчика')
		for s in range(1, len(function_t)):	#Спобоб2
			if len(self.signal_noise_norm_distr) > int(function_t[s]) and len(signal_noise_norm_distr)>int(function_t[s]):
				if signal_noise_norm_distr[int(function_t[s])] > (self.signal_noise_norm_distr[int(function_t[s])]):
					true_signal_candidate.append((function_t[s], s))
		# for s in range(1, len(function_t)):	#Превращаем сигнал в данные
			# if function_t[s] >= noise_exp_value/exp_val*max(function_t):	#Задаем порог способ1
				# true_signal_candidate.append((function_t[s], s))
		if len(true_signal_candidate)>len(request_codes[0]):
			for i in range(len(request_codes[0])):
				index=true_signal_candidate.index(max(true_signal_candidate))
				recv_time.append(true_signal_candidate[index][1])	#Добавляем промежутки между сигналами [ms]
				del true_signal_candidate[index]
		else:
			for i in range(len(true_signal_candidate)):
				recv_time.append(true_signal_candidate[i][1])	#Добавляем промежутки между сигналами [ms]
		code_index = find_code(recv_time, request_codes)
		False_signals, target_loss = error_analyzer(request_codes[code_index], recv_time)	#Анализируем ошибки
		msg.append('################################')
		msg.append('Потерь сигнала ответчика: '+ str(target_loss)+'. Ложные срабатывания ответчика: '+ str(False_signals))
		send_code(requester1, answer_codes[code_index])
	
class channel:
	def __init__(self, distance, mu, sigma, noise_ampl):
		self.wait_time = distance*10**3/speed_of_light	#s
		self.mu = mu
		self.sigma = sigma
		self.noise_ampl = noise_ampl
		print(self.wait_time, 'wait_time')

	def start(self, receiver, function_t):
		time.sleep(self.wait_time)
		for i in range(len(function_t)):	#Добавляем помехи и шум
			RandVal = random.gauss(0, self.noise_ampl)
			for k in range(len(self.sigma)):	#генерим полинормальные помехи
				RandVal += random.gauss(self.mu[k], self.sigma[k])
			function_t[i] += RandVal if RandVal > 0 else 0
		receiver.recv(function_t)

def find_code(recv_time, sender_codes):	#Находим индекс кода более похожего на определенный код запроса
	subtraction = [0]*len(sender_codes)
	for i in range(len(sender_codes)):
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
			function_t.append(amplitude)
		else:
			function_t.append(0)
	channel1.start(receiver, function_t)	#отправляем функцию (последовательность)

def find_expected_value(signal_noise_norm_distr, function_t):
	normalized_snn_distr = []
	exp_val = 0
	for i in range(len(function_t)):	#Переводим все в int, чтобы было легче построить распределение 
		function_t[i] = int(function_t[i])

	if max(function_t)+1 - len(signal_noise_norm_distr) > 0:
		for  i in range(max(function_t)+1 - len(signal_noise_norm_distr)):	#Создаем список распределения величин, согласно максимальной амплитуде сигнала
			signal_noise_norm_distr.append(0)

	for i in range(len(function_t)):	#Создаем/дополняем распределение амплитуд сигналов
		signal_noise_norm_distr[function_t[i]] += function_t[i]

	for i in range(len(signal_noise_norm_distr)):
		normalized_snn_distr.append(signal_noise_norm_distr[i]/sum(signal_noise_norm_distr))	#Нормируем распределение

	for i in range(len(normalized_snn_distr)):
		exp_val +=  normalized_snn_distr[i]*i 	#Рассчитываем мат ожидание

	return signal_noise_norm_distr, exp_val

def error_analyzer(codes, recv_time):
	True_signals = 0
	target_loss = 0
	for code_time in codes:	#Подсчитываем кол-во ошибок
		if code_time in recv_time:
			True_signals += 1
		else:
			target_loss +=1		
	Q_errors = len(recv_time) - True_signals if len(recv_time)>len(codes) else len(codes) - True_signals	#Ошибки
	False_signals = Q_errors - target_loss	#Ложные срабатывания
	return False_signals, target_loss

def analyze_noise(mu, sigma, noise_ampl):
	signal_noise_norm_distr = []
	max_time = 0
	for code in answer_codes:	#Находим максимальную длительность сообщения
		max_time_temp = max(code)
		max_time = max_time_temp if max_time_temp>max_time else max_time
	for i in range(1000):
		noise = []
		for i in range(max_time):	#Создаем шум
			RandVal = random.gauss(0, noise_ampl)
			for k in range(len(mu)):	#И помехи
				RandVal += random.gauss(mu[k], sigma[k])
			noise.append(RandVal)
		signal_noise_norm_distr, noise_exp_val = find_expected_value(signal_noise_norm_distr, noise)	#Анализируем шум
	return signal_noise_norm_distr, noise_exp_val 	#Выдаем мат ожидание шума

# def likehood_func(signal_noise_norm_distr, function_t):
# 	signal_noise_norm_distr, exp_val = find_expected_value(signal_noise_norm_distr, function_t)	#ищем мат ожидание
# 	likehood = math.exp(3*) 

def requester1_send(_):
	requester1.send()
	return requester1.False_signals, requester1.target_loss, requester1.distance, requester1.time_measured

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
	words_in_line = 32
	for messages in msg:
		while len(messages)>words_in_line:
			line_msg.append(messages[:words_in_line])
			messages = messages[words_in_line:]
		line_msg.append(messages)
	for i in range(len(line_msg)):
		msg_ts = textfont.render(line_msg[i], False, light_yellow)	#рендерим сообщения от программы
		gameDisplay.blit(msg_ts, (display_width//5*2, int(display_heigth*(0.05+i*0.1))))

pygame.init()	#Запускаем pygame
pygame.font.init()
textfont = pygame.font.SysFont('Comic Sans MS', 28)	#инициализируем шрифт

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
mu = [90, 20, 70]	#Среднее значение шума
sigma = [40, 60, 10]	#Отклонение от ср значения
noise_ampl = 10	#Средняя амплитуда шума
amplitude = 100
####################################################
send_Q = 100
code_index = 1
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
				False_signals_temp, target_loss_temp, distance_temp, time_measured_temp = 0, 0, 0, 0
				channel1 = channel(distance, mu, sigma, noise_ampl)	#Агрумент -- расстояние в км
				requester1 = requester(code_index) #Создаем объекты
				answerer1 = answerer()
				signal_noise_norm_distr, noise_exp_value = analyze_noise(mu, sigma, noise_ampl)
				msg.append('кол-во итераций: '+str(send_Q))
				msg.append('Заданная дистанция: '+str(distance))
				with Pool(4) as p:
					data  = p.map(requester1_send, [0]*send_Q)	#Отправляем запросы
				for step in data:
					False_signals_temp += step[0]
					target_loss_temp += step[1]
					distance_temp += step[2]
					time_measured_temp += step[3]
				msg.append('Средняя дистанция: '+str(round(distance_temp/send_Q,2))+' km')
				msg.append('Средний интервал: ' + str(round(time_measured_temp*10**6/send_Q,2)) + ' us')
				msg.append('Потерь сигнала: '+ str(round(target_loss_temp/(send_Q*len(answer_codes)+1)*100))+'%')
				msg.append('Ложные срабатывания: '+  str(round(False_signals_temp/(send_Q*len(answer_codes)+1)*100))+'%')
			elif -button_size[0]/2<=mouse[0]-button_left_xy[0]<=button_size[0]/2 and -button_size[1]/2<=mouse[1]-button_left_xy[1]<=button_size[1]/2:
				code_index = decrease_code_index(code_index)
			elif -button_size[0]/2<=mouse[0]-button_right_xy[0]<=button_size[0]/2 and -button_size[1]/2<=mouse[1]-button_right_xy[1]<=button_size[1]/2:
				code_index = increase_code_index(code_index)
			elif -button_size[0]/2<=mouse[0]-button_random_code_xy[0]<=button_size[0]/2 and -button_size[1]/2<=mouse[1]-button_random_code_xy[1]<=button_size[1]/2:
				code_index = random.randint(0, len(request_codes)-1)
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