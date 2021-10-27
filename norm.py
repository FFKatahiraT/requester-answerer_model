import random
import matplotlib.pyplot as plt 

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

	# print(len(normalized_snn_distr), 'len(normalized_snn_distr)')
	# print(normalized_snn_distr, 'normalized_snn_distr')
	for i in range(len(normalized_snn_distr)):
		exp_val +=  normalized_snn_distr[i]*i 	#Рассчитываем мат ожидание
		print(exp_val, 'exp_val')

	return signal_noise_norm_distr, exp_val

a = []
b = []
n = 10**5
mu = 100
sigma = 10
for i in range(n):
	a.append(int(random.gauss(mu, sigma)))

for  i in range(max(a)+1):
	b.append(0)

for i in range(n):
	b[a[i]] += a[i]

print(find_expected_value(b,a)[1])

plt.plot(range(max(a)+1), b)
plt.show()