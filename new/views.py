from django.http import HttpResponse, HttpRequest
from django.shortcuts import redirect
from django.shortcuts import render_to_response
from django.shortcuts import render
from forms import MessageForm
from zipfile import *
import shutil
import os
from os import listdir
from os.path import isfile, join
import qrcode
import requests
import json

import math
preobrazoborudovanie=25100+69471+23781+64600
srokdeistvia = 15
a=0
stoimcontroller = 9779
stoimbatarei = 26300
stoiminvertorout = 9613
stoiminvertorin = 7800
stoimvetrogen = 99157
stoimsolnbat = 29000
estlivigodnie = 0
stoimakkumul = 37900
emkostakkumul = 250
spisokvozmozhnihvie = [1, 1, 1]
bd=''

def API(request):
	s = ""
	d=''
	if request.method == 'GET':
		resp = HttpResponse()
		resp.status_code = 200

		resp.write(s)
		resp.write(d)
		return resp

	resp = HttpResponse()
	resp.status_code = 204
	resp.write('We need a request')
	return resp


def MINIGES(request):
	estlivigodnie = 0
	s = ""
	if request.method == 'GET':
		resp = HttpResponse()
		resp.status_code = 200
		nomerregion =  int(request.GET.get('region'))
		spisokregionov = ['Саратовская область','Ульяновская область','Московская область','Ростовская область']
		region = spisokregionov[nomerregion]
		spvreki = [2.4, 3.1, 2.2, 3.3]	
		spvvetra = [4, 5, 6, 4.2]
		spesolnca = [1100,950,1010,1290]
		sptarif = [3.43, 3.68, 3.83, 5.38]
		moshn = float(request.GET.get('moshn'))
		indexregionavspiske = 0
		for i in spisokregionov:
			if i == region:
				vreki = spvreki[indexregionavspiske]
				vvetra = spvvetra[indexregionavspiske]
				esolnca = spesolnca[indexregionavspiske]
				tarif = sptarif[indexregionavspiske]
			indexregionavspiske += 1
		if vreki > 0:
			if vreki < 1:
				tipmikroges = 'Плотинные '
				stoimost = [44700, 64900 ,68000]
				moshnmikroges = [1, 2, 3]
				kolvomikroges = [0, 0, 0]
				kolvomikroges[2] = moshn // 3
				if moshn % 3 > 2:
					kolvomikroges[2] += 1
				kolvomikroges[2] = int(kolvomikroges[2])
				if (moshn - kolvomikroges[2] * 3) > 1:
					kolvomikroges[1] = 1
				kolvomikroges[1] = int(kolvomikroges[1])
				if (moshn - kolvomikroges[2] * 3 - kolvomikroges[1] * 2) > 0:
					kolvomikroges[0] = 1
				kolvomikroges[0] = int(kolvomikroges[0])
				summamikroges = stoimost[0] * kolvomikroges[0] + stoimost[1] * kolvomikroges[1] + stoimost[2] * kolvomikroges[2] + stoimcontroller + stoimbatarei + stoiminvertorout + stoiminvertorin
				if moshn * 365 * 24 * srokdeistvia * tarif > summamikroges: 
					print("Плотинные МиниГЭС ставить выгодно, прибыль составляет: ", int(moshn * 365 * 24 * srokdeistvia * tarif - summamikroges), 'рублей')
					estlivigodnie += 1
				else:
					print("Плотинные МиниГЭС ставить невыгодно, убыток составляет: ",int(moshn * 365 * 24 * srokdeistvia * tarif - summamikroges), 'рублей')
				indexmoshnmikroges=0
				print('Необходимо: ')
				for i in kolvomikroges:
					if i != 0:
						print(i, 'МиниГЭС с мощностью', moshnmikroges[indexmoshnmikroges], 'кВтч ')
					indexmoshnmikroges+=1
				print('Стоимость постройки составляет',summamikroges, 'рублей')
				a = moshn * 365 * 24 * srokdeistvia * tarif - summamikroges
			else:
				tipmikroges = 'Деривационные'
				stoimost = [44700, 64900 ,68000]
				moshnmikroges = [1, 2, 3]
				kolvomikroges = [0, 0, 0]
				kolvomikroges[2] = moshn // 3
				if moshn % 3 > 2:
					kolvomikroges[2] += 1
				kolvomikroges[2] = int(kolvomikroges[2])
				if (moshn - kolvomikroges[2] * 3) > 1:
					kolvomikroges[1] = 1
				kolvomikroges[1] = int(kolvomikroges[1])
				if (moshn - kolvomikroges[2] * 3 - kolvomikroges[1] * 2) > 0:
					kolvomikroges[0] = 1
				kolvomikroges[0] = int(kolvomikroges[0])
				summamikroges = stoimost[0] * kolvomikroges[0] + stoimost[1] * kolvomikroges[1] + stoimost[2] * kolvomikroges[2] + stoimcontroller + stoimbatarei + stoiminvertorout + stoiminvertorin
				if moshn * 365 * 24 * srokdeistvia * tarif > summamikroges: 
					ss="Деривационные МиниГЭС ставить выгодно, прибыль составляет:" + str(int(moshn * 365 * 24 * srokdeistvia * tarif - summamikroges)) +' ' + 'рублей. '
					estlivigodnie = estlivigodnie + 1
				else:
					ss="Деривационные МиниГЭС ставить невыгодно, убыток составляет:" + str(int(moshn * 365 * 24 * srokdeistvia * tarif - summamikroges)) + ' ' + 'рублей. '
				indexmoshnmikroges=0
				ss += 'Необходимо: '
				for i in kolvomikroges:
					if i != 0:
						ss += str(i) + ' ' + 'МиниГЭС с мощностью' + ' ' + str(moshnmikroges[indexmoshnmikroges]) + ' ' + 'кВтч;' 
					indexmoshnmikroges+=1
				s='Стоимость постройки составляет' + ' ' + str(summamikroges) + ' ' + 'рублей'
				a = moshn * 365 * 24 * srokdeistvia * tarif - summamikroges
		else:
			s='Постройка МиниГЭС нерациональна в связи с условиями окружающей среды'
			a = 0
			spisokvozmozhnihvie[0] = 0
		resp.write(ss)
		resp.write(' ')
		resp.write(s)
		return resp

	resp = HttpResponse()
	resp.status_code = 204
	resp.write('We need a request')
	return resp


def VETROGEN(request):
	estlivigodnie = 0
	s = ""
	if request.method == 'GET':
		resp = HttpResponse()
		resp.status_code = 200
		if vvetra > 0.7:
			if vvetra > 3:
				tipvetrogen = 'Горизонтальные'
				moshnvetrogen = 2.5
				kolvovetrogen = moshn // moshnvetrogen + 1
				summavetrogen = stoimvetrogen * kolvovetrogen + stoimbatarei + stoimcontroller + stoiminvertorout + stoimakkumul * math.ceil(moshn * 1000 / 0.8 / emkostakkumul * 2) + stoiminvertorin
				if moshn * 365 * 24 * srokdeistvia * tarif > summavetrogen: 
					s += "Горизонтальные Ветрогенераторы ставить выгодно, прибыль составляет:" + str(int(moshn * 365 * 24 * srokdeistvia * tarif - summavetrogen)) + ' ' + 'рублей'
					estlivigodnie += 1
				else:
					s += "Горизонтальные Ветрогенераторы ставить невыгодно, убыток составляет:"+  str(int(moshn * 365 * 24 * srokdeistvia * tarif - summavetrogen)) + ' ' + 'рублей'
				b = moshn * 365 * 24 * srokdeistvia * tarif - summavetrogen
				s+='. Необходимо ветрогенераторов:' + ' ' +  str(int(kolvovetrogen))
				s += '. Стоимость постройки составляет: ' + str(int(summavetrogen)) + ' ' + ' рублей '
			else:
				tipvetrogen = 'Вертикальные'
				moshnvetrogen = 2.5
				kolvovetrogen = moshn // moshnvetrogen + 1
				summavetrogen = stoimvetrogen * kolvovetrogen + stoimbatarei + stoimcontroller + stoiminvertorout + stoimakkumul * math.ceil(moshn * 1000 / 0.8 / emkostakkumul * 2) + stoiminvertorin
				if moshn * 365 * 24 * srokdeistvia * tarif > summavetrogen: 
					s += "Вертикальные Ветрогенераторы ставить выгодно, прибыль составляет:" +  str(int(moshn * 365 * 24 * srokdeistvia * tarif - summavetrogen)) + ' ' + 'рублей'
					estlivigodnie += 1
				else:
					s += "Вертикальные Ветрогенераторы ставить невыгодно, убыток составляет:" +  str(int(moshn * 365 * 24 * srokdeistvia * tarif - summavetrogen)) + ' ' + 'рублей'
				b = moshn * 365 * 24 * srokdeistvia * tarif - summavetrogen
				s += 'Необходимо ветрогенераторов:' + ' ' + str(int(kolvovetrogen))
				s += 'Стоимость постройки составляет:' + ' ' + str(int(summavetrogen)) + ' ' + ' рублей '
		else:
			s='Установка ветрогенераторов нерациональна в связи с условиями окружающей среды '
			b = 0
			spisokvozmozhnihvie[1] = 0
		
		resp.write(s)
		return resp

	resp = HttpResponse()
	resp.status_code = 204
	resp.write('We need a request')
	return resp

def SOLNBAT(request):
	estlivigodnie = 0
	s = ""
	if request.method == 'GET':
		resp = HttpResponse()
		resp.status_code = 200
		nomerregion =  int(request.GET.get('region'))

		spisokregionov = ['Саратовская область','Ульяновская область','Московская область','Ростовская область']
		region = spisokregionov[nomerregion]
		spvreki = [2.4, 3.1, 2.2, 3.3]	
		spvvetra = [4, 5, 6, 4.2]
		spesolnca = [1100,950,1010,1290] 
		sptarif = [3.43, 3.68, 3.83, 5.38]
		moshn = float(request.GET.get('moshn'))
		indexregionavspiske = 0
		for i in spisokregionov:
			if i == region:
				vreki = spvreki[indexregionavspiske]
				vvetra = spvvetra[indexregionavspiske]
				esolnca = spesolnca[indexregionavspiske]
				tarif = sptarif[indexregionavspiske]
			indexregionavspiske += 1
		if esolnca > 1050:
			moshnsolnbat = 0.29 
			kolvosolbat = moshn // moshnsolnbat + 1
			summasolnbat = stoimsolnbat * kolvosolbat + stoimbatarei + stoimcontroller + stoiminvertorout + stoimakkumul * math.ceil(moshn * 1000 / 0.8 / emkostakkumul * 2) + stoiminvertorin
			if moshn * 365 * 24 * srokdeistvia * tarif > summasolnbat: 
				s += "Солнечные панели ставить выгодно, прибыль составляет: " +  str(int(moshn * 365 * 24 * srokdeistvia * tarif - summasolnbat)) + ' рублей'
				estlivigodnie += 1
			else:
				s += "Солнечные панели ставить невыгодно, убыток составляет: " + str(int(moshn * 365 * 24 * srokdeistvia * tarif - summasolnbat)) + ' рублей'
			c = moshn * 365 * 24 * srokdeistvia * tarif - summasolnbat
			s += '. Необходимо солнечных панелей: ' +  str(int(kolvosolbat))
			s += '. Стоимость постройки составляет: ' +  str(int(summasolnbat)) + ' рублей '
		else:
			s = 'Установка солнечных панелей нерациональна в связи с условиями окружающей среды '
			c = 0
			spisokvozmozhnihvie[2] = 0
		resp.write(s)
		return resp

	resp = HttpResponse()
	resp.status_code = 204
	resp.write('We need a request')
	return resp


def VIBOR(request):
	estlivigodnie = 0
	s = ""
	if request.method == 'GET':
		resp = HttpResponse()
		resp.status_code = 200
		nomerregion =  str(request.GET.get('region'))
		lng = float(request.GET.get('lng'))
		ltg = float(request.GET.get('ltg'))
		spisokregionov = ['Чукотский автономный округ','Республика Саха (Якутия)','Тамбовская область','Республика Алтай']
		region = nomerregion
		srokrabvetrogen=22
		tipmikroges=''
		tipvetrogen=''
		srokrabotsolnbat=15
		srokrabotmicroges=11
		vreki = 0
		vvetra = 0
		indexregionavspiske = 0
		spgorod=[['Анадырь','Билибино','Биллингс (Чаунский район)','Илирней (Билибинский р-н)','Канчалан (Анадырский р-н)','Марково (Анадырский р-н)','Омолон (Билибинский р-н)','Певек','Провидения','Уэлен (Чукотский район)','Эгвекинот'],['Якутск','Алдан','Амга','Андрюшкино (Нижнеколымский район)','Батагай','Батагай-Алыта','Белая Гора','Бердигестях','Бестях (Жиганский район)','Верхневилюйск','Верхоянск','Вилюйск','Витим (Ленский район)','Депутатский','Жиганск','Жилинда (Оленёкский р-н)','Исит (Хангаласский р-н)','Казачье (Усть-Янский р-н)','Колымское (Нижнеколымский район)','Крестях (Сунтарский р-н)','Крест-Хальджай (Томпонский район)','Кюсюр (Булунский район)','Ленск','Мача (Олёкминский район)','Мирный','Намцы','Нюрба','Оймякон','Олёкминск','Оленёк','Покровск','Сангар','Саскылах','Себян-Кюёль (Кобяйский район)','Среднеколымск','Сунтар','Тёплый Ключ (Томпонский район)','Тикси','Томмот (Алданский район)','Тяня (Олёкминский район)','Усть-Куйга (Усть-Янский район)','Усть-Мая','Усть-Нера','Хонуу','Чагда (Алданский район)','Чернышевский (Мирнинский район)','Черский','Чокурдах','Чульман (Нерюнгринский район)','Чурапча','Эйик (Оленёкский район)'],['Тамбов','Жердевка','Кирсанов','Мичуринск','Моршанск','Новопокровка','Уварово'],['Горно-Алтайск','Артыбаш','Катанда','Кош-Агач','Майма','Онгудай','Турочак','Усть-Кан','Усть-Кокса','Чемал','Шебалино']]
		spvvvetra = [  [[7.4, 6.4, 6.2, 6.6],[1.2, 2.4, 2.3 ,1.7],[4.8, 4.6, 5.8, 5.2],[0.7, 1.6, 1.9, 1.3],[5.0, 3.9, 3.9, 4.6],[1.9, 2.1, 2.2, 2.0],[0.5, 1.7, 2.0, 1.4],[3.0,3.7, 4.6, 4.1],[4.9,3.4, 3.5 ,4.2],[5.7, 4.3, 5.5, 6.9],[4.7, 3.9, 3.3, 4.0]]  ,  [[0.8, 1.9, 2.1, 1.7],[1.2, 1.8, 1.4, 1.5],[0.7, 2.0, 2.1, 1.6],[2.3, 2.8, 4.0, 2.8],[1.1, 2.3, 2.8, 2.0],[0.9, 2.0, 2.3, 1.4],[0.8, 2.0, 3.0, 1.7],[0.6, 1.6, 1.4, 1.3],[1.1, 1.7, 1.8, 1.5],[1.4, 2.0, 2.0, 1.9],[0.5, 1.2, 1.6, 1.0],[1.3, 1.9, 2.0, 1.8],[1.6, 2.2, 2.1, 2.2],[2.2, 2.6, 3.1, 2.3],[1.9, 2.8, 2.7, 2.2],[1.3, 1.9, 1.7, 1.4],[1.5, 1.3, 1.4, 1.6],[2.5, 2.8, 3.6, 2.8],[2.7, 3.0, 3.4, 3.0],[0.8, 1.7, 1.7, 1.6],[0.2, 1.4, 1.3, 1.2],[1.8, 3.3, 3.5, 2.5],[2.7, 2.6, 2.2, 2.6],[1.2, 1.9, 1.8, 1.9],[2.6, 3.0, 2.6, 3.0],[0.7, 2.0, 2.1, 1.6],[1.6, 2.3, 2.0, 2.0],[0.4, 1.6, 2.1, 1.3],[2.1, 2.8, 2.2, 2.4],[1.5, 2.8, 2.9, 2.3],[1.8, 2.6, 2.6, 2.4],[1.8, 3.2, 3.3, 3.1],[3.3, 3.6, 4.1, 3.5],[0.6, 1.4, 1.3, 0.9],[1.2, 1.7, 2.0, 1.5],[1.3, 1.9, 1.8, 1.8],[0.7, 1.6, 1.5, 1.1],[5.4, 3.8, 4.4, 5.1],[0.5, 1.1, 1.0, 0.9],[0.2, 0.8, 0.6, 0.5],[1.2, 2.1, 2.9, 1.6],[0.4, 1.9, 1.9, 1.5],[0.6, 2.5, 2.6, 2.2],[0.2, 1.5, 2.1, 1.0],[1.3, 1.4, 1.1, 1.6],[3.7, 3.5, 3.0, 3.5],[2.3, 2.7, 3.1, 2.4],[3.7, 3.6, 4.2, 3.5],[2.3, 3.4, 3.3, 3.1],[0.5, 1.9, 2.0, 1.6],[1.5, 2.3, 2.0, 2.2]],  [[3.7,3.5,2.9,3.4],[3.1,2.9,2.3,2.8],[2.7,2.5,2.0,2.4],[2.4,2.0,1.6,1.9],[2.7,2.4,2.0,2.3],[2.6,2.4,1.9,2.2],[3.3,2.9,2.3,3.0]]  ,  [[1.0, 1.4, 1.3, 1.3],[2.1, 1.5, 1.2, 1.8],[0.7, 1.6, 1.4, 1.3],[0.4, 1.9, 1.5, 1.0],[1.5, 2.6, 2.1,1.9],[0.4, 0.9, 0.8, 0.6],[0.4, 1.3, 1.1, 0.9],[0.8, 1.3, 1.0, 0.9],[0.7, 1.6, 1.4, 1.1],[1.3, 0.9, 0.8, 1.1],[1.4, 2.0, 1.7, 1.7]] 	]
		coordstowns=[ [[177.508924, 64.733115], [166.451139, 68.057129], [108.504395, 45.782786], [168.331349, 67.360853], [176.610339, 65.178518], [170.406987, 64.681627], [160.537592, 65.235572], [170.299935, 69.701761], [173.218911, 64.427404], [169.817611, 66.160148], [177.339546, 68.087557]], [[129.732663, 62.028103], [125.381673, 58.609451], [131.976807, 60.900648], [154.444948, 69.172622], [134.627853, 67.654523], [130.397632, 67.799054], [146.18396, 68.538155], [123.064819, 62.294199], [124.499024, 66.260042], [120.315561, 63.445995], [133.390702, 67.550161], [121.627326, 63.751722], [112.557809, 59.429471], [139.950523, 69.340813], [123.374226, 66.767581], [113.988035, 70.139367], [125.326687, 60.812127], [136.208133, 70.744575], [158.704472, 68.727784], [116.166, 62.256879], [134.518043, 62.811728], [127.361695, 70.686205], [114.911844, 60.713731], [117.700808, 60.065925], [113.978692, 62.541028], [129.661579, 62.719322], [118.324239, 63.282823], [125.519735, 67.485269], [120.406013, 60.375796], [136.980648, 60.01414], [129.148219, 61.48424], [127.46642, 63.923462], [112.600452, 68.355097], [130.008392, 65.288282], [153.707009, 67.458183], [117.647601, 62.160619], [136.850419, 62.7875], [128.870846, 71.638912], [126.287579, 58.958666], [120.258536, 58.969861], [135.548805, 70.004222], [134.540734, 60.415628], [143.232195, 64.567743], [143.218774, 66.455175], [130.607964, 58.750285], [112.468867, 63.018836], [161.333086, 68.751114], [147.90065, 70.620662], [124.904632, 56.840582], [132.440572, 61.996629], [117.379768, 66.006895]], [[41.452274, 52.721219], [41.461796, 51.842282], [42.728663, 52.650646], [40.498011, 52.893913], [41.811627, 53.443611], [74.730947, 42.869322], [42.261, 51.983099]], [[85.960373, 51.958182], [87.265356, 51.792994], [86.177532, 50.164731], [88.661661, 49.99647], [85.89618, 52.003718], [86.133775, 50.749658], [87.121653, 52.257527], [84.762263, 50.929383], [85.616067, 50.268979], [86.001417, 51.407744], [85.674197, 51.292099]]]
		#for i in spisokregionov:
		#	for j in spgorod[indexregionavspiske]:
		#		strzapr='https://geocode-maps.yandex.ru/1.x/?format=json&geocode='+j
		#		zapros = requests.get(strzapr)
		#		pamyt = json.loads(zapros.text)
		#		coordst = pamyt['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['Point']['pos'].split(' ')
		#		coordstowns[indexregionavspiske].append([float(coordst[0]),float(coordst[1])])
		#	indexregionavspiske+=1	
		#bd=coordstowns
		esolnca=0
		spvvetra=[3,5,7,6]
		spvreki = [ 1.42, 1.87,0.48,0.36]
		spesolnca = [5.17,5.21,5.79,6.8]
		sptarif = [8.2, 5.95, 3.83, 6.3]
		spnerabrek = [4/12*365,5/12*365,7/12*365,8/12*365]
		sprabsolca=[2360,2502,2120,4000]
		rabsolnca = 0
		rabrek = 0
		c=0
		moshn = float(request.GET.get('moshn'))
		minrazn=1000
		minrazn=float(minrazn)
		indexoftowns=0
		summasolnbat=0
		kolvobat=0
		kolvobat=moshn
		moshn=moshn*0.6
		ppot=moshn*0.3
		moshn=moshn+ppot
		indexregionavspiske = 0
		for i in spisokregionov:
			if i == region:
				vreki = spvreki[indexregionavspiske]
				#vvetra = spvvetra[indexregionavspiske]
				esolnca = spesolnca[indexregionavspiske]
				tarif = sptarif[indexregionavspiske]
				rabrek=spnerabrek[indexregionavspiske]
				rabsolnca=sprabsolca[indexregionavspiske]
				for j in coordstowns[indexregionavspiske]:
					if float(( (j[0]-ltg)**2+(j[1]-lng)**2 )**0.5)<minrazn:
						minrazn=( (j[0]-ltg)**2+(j[1]-lng)**2 )**0.5
						vvetra=min(spvvvetra[indexregionavspiske][indexoftowns])
					indexoftowns+=1	

			indexregionavspiske += 1
		if vreki > 0:
			if vreki < 1:
				stoimplot=10000
				tipmikroges = ' Плотинные '
				stoimost = [44700+700000, 64900+700000 ,68000+700000,139000+700000]
				moshnmikroges = [1, 2, 3, 5]
				kolvomikroges = [0, 0, 0, 0]
				kolvomikroges[3] = moshn // 5
				kolvomikroges[2] = (moshn-kolvomikroges[3]*5) // 3
				if moshn % (moshnmikroges[2]) > 2:
					kolvomikroges[2] += 1
				kolvomikroges[2] = int(kolvomikroges[2])
				if (moshn - kolvomikroges[2] * 3) > 1:
					kolvomikroges[1] = 1
				kolvomikroges[1] = int(kolvomikroges[1])
				if (moshn - kolvomikroges[2] * 3 - kolvomikroges[1] * 2) > 0:
					kolvomikroges[0] = 1
				kolvomikroges[0] = int(kolvomikroges[0])
				summamikroges =stoimost[3] * kolvomikroges[3]+ stoimost[0] * kolvomikroges[0]  + stoimost[1] * kolvomikroges[1] + stoimost[2] * kolvomikroges[2] + preobrazoborudovanie + tarif* rabrek *moshn
				if moshn * 365 * srokrabotmicroges * tarif > summamikroges: 
					s+=" Плотинные МиниГЭС ставить выгодно, прибыль составляет: "
					s+=str(int(moshn * 365 * srokdeistvia * tarif - summamikroges))
					s+='рублей'
					estlivigodnie += 1
					s+='Необходимо:'
					for i in kolvomikroges:
						if i != 0:
							s+='МиниГЭС с мощностью ' + str(moshnmikroges[indexmoshnmikroges]) + ' кВт '
						indexmoshnmikroges+=1
					s+='Стоимость постройки составляет ' + str(summamikroges) + 'рублей, '
					a = moshn * 365 * srokrabotmicroges * tarif - summamikroges
				else:
					s="МиниГЭС ставить невыгодно, "
				indexmoshnmikroges=0
				
			else:
				tipmikroges = 'Деривационные '
				stoimost = [44700+700000, 64900+700000 ,68000+700000,139000+700000]
				moshnmikroges = [1, 2, 3, 5]
				kolvomikroges = [0, 0, 0, 0]
				kolvomikroges[3] = moshn // 5
				kolvomikroges[2] = (moshn-kolvomikroges[3]*5) // 3
				if (moshn-kolvomikroges[3]*5-kolvomikroges[2]*3) % 3 > 2:
					kolvomikroges[2] += 1
				kolvomikroges[3] = int(kolvomikroges[3])
				kolvomikroges[2] = int(kolvomikroges[2])
				if (moshn - kolvomikroges[2] * 3) > 1:
					kolvomikroges[1] = 1
				kolvomikroges[1] = int(kolvomikroges[1])
				if (moshn - kolvomikroges[2] * 3 - kolvomikroges[1] * 2-kolvomikroges[3]*5) > 0:
					kolvomikroges[0] = 1
				kolvomikroges[0] = int(kolvomikroges[0])
				summamikroges =stoimost[3] * kolvomikroges[3]+ stoimost[0] * kolvomikroges[0] + stoimost[1] * kolvomikroges[1] + stoimost[2] * kolvomikroges[2] + preobrazoborudovanie  + tarif*rabrek*moshn
				if moshn * 365 * srokrabotmicroges * tarif > summamikroges: 
					s+="Деривационные МиниГЭС ставить выгодно, прибыль составляет: " + str(int(moshn * 365 * srokrabotmicroges * tarif - summamikroges)) +' ' + 'рублей. '
					estlivigodnie = estlivigodnie + 1
					s += 'Необходимо: '
					for i in kolvomikroges:
						if i != 0:
							s += str(i) + ' ' + 'МиниГЭС с мощностью ' + ' ' + str(moshnmikroges[indexmoshnmikroges]) + ' ' + 'кВт;\n' 
						indexmoshnmikroges+=1
					s+='Стоимость постройки составляет: ' + ' ' + str(int(summamikroges*10//10)) + ' ' + 'рублей;\n\n'
					a = moshn * 365 * srokrabotmicroges * tarif - summamikroges
					s+="прибыль:"+str(int(a)) + ' рублей, '
				else:
					s+="МиниГЭС ставить невыгодно, "
				indexmoshnmikroges=0
		else:
			s='Постройка МиниГЭС нерациональна в связи с условиями окружающей среды \n'
			a = 0
			spisokvozmozhnihvie[0] = 0
		q=''

		if vvetra > 2:
			spmoshnvetrogen=[1,2,3,4]
			spkolvovetrogen=[0,0,0,0]
			spstoimvetrogen=[65000,80000,110000,119000]
			spkolvovetrogen[3]=moshn//spmoshnvetrogen[3]
			spkolvovetrogen[3]=int(spkolvovetrogen[3])
			if moshn-spkolvovetrogen[3]*4>3:
				spkolvovetrogen[3]+=1
			spkolvovetrogen[3]=int(spkolvovetrogen[3])
			if moshn-spkolvovetrogen[3]*4>2:
				spkolvovetrogen[2]+=1
			spkolvovetrogen[2]=int(spkolvovetrogen[2])	
			if moshn-spkolvovetrogen[3]*4-spkolvovetrogen[2]*3>1:
				spkolvovetrogen[1]+=1
			spkolvovetrogen[1]=int(spkolvovetrogen[1])	
			if moshn-spkolvovetrogen[3]*4-spkolvovetrogen[2]*3-spkolvovetrogen[1]*2>0:
				spkolvovetrogen[0]+=1
			spkolvovetrogen[0]=int(spkolvovetrogen[0])	
			e=0.45
			nmax=0
			maxdnvetr=0
			r=1
			a=0
			#spdnvetra=[[0,0,0,1,5,6,3,2,1,3,6,7,5,6,5,3,6,8,9,6,3,1,4,5,5,4,2,1,7,2],[1,2,3,4,5,6,3,2,1,3,6,7,5,6,5,3,6,8,9,6,3,1,4,5,5,4,2,1,7,2],[1,2,3,4,5,6,3,2,1,3,6,7,5,6,5,3,6,8,9,6,3,1,4,5,5,4,2,1,7,2],[1,2,3,4,5,6,3,2,1,3,6,7,5,6,5,3,6,8,9,6,3,1,4,5,5,4,2,1,7,2]]
			#for i in spdnvetra[0]:
			#	if i<=1:
			#		maxdnvetr+=1
			#	else:
			#		if maxdnvetr>nmax:
			#			nmax=maxdnvetr
			#		maxdnvetr=0	

			if vvetra > 3:
				indexmoshnmikroges=0
				tipvetrogen = 'Пропеллерные '
				#moshnvetrogen = e*vvetra**3*1.29*3.14*r**2/2
				summavetrogen = spstoimvetrogen[0] * spkolvovetrogen[0] + spstoimvetrogen[1] * spkolvovetrogen[1] + spstoimvetrogen[2] * spkolvovetrogen[2] +  spstoimvetrogen[3] * spkolvovetrogen[3] +preobrazoborudovanie
				if moshn * 365 * srokrabvetrogen * tarif > summavetrogen: 
					q += "Пропеллерные ветрогенераторы ставить выгодно, прибыль составляет: " + str(int(moshn * 365 * srokrabvetrogen * tarif - summavetrogen)) + ' ' + 'рублей, '
					estlivigodnie += 1
					b = moshn * 365 * srokrabvetrogen * tarif - summavetrogen
					q+="Необходимо:"
					for i in spkolvovetrogen:
						if i != 0:
							q += str(int(i)) + ' ' + ' с мощностью ' + ' ' + str(spmoshnvetrogen[indexmoshnmikroges]) + ' ' + 'кВт;\n' 
						indexmoshnmikroges+=1
					q += 'Затраты составляют: ' + str(int(summavetrogen)) + ' ' + 'рублей; '
					q+="Прибыль: "+str(int(b))+ ' рублей, '
				else:
					q += "Ветрогенераторы ставить невыгодно, "
				
			else:
				tipvetrogen = 'Вертикальные'
				#moshnvetrogen = e*vvetra**3*1.29*3.14*r**2/2
				summavetrogen = spstoimvetrogen[0] * spkolvovetrogen[0] + spstoimvetrogen[1] * spkolvovetrogen[1] + spstoimvetrogen[2] * spkolvovetrogen[2] +  spstoimvetrogen[3] * spkolvovetrogen[3] + preobrazoborudovanie
				if moshn * 365 * srokrabvetrogen * tarif > summavetrogen: 
					q += "Вертикальные Ветрогенераторы ставить выгодно, прибыль составляет: " +  str(int(moshn * 365 * srokrabvetrogen * tarif - summavetrogen)) + ' ' + 'рублей'
					estlivigodnie += 1
					b = moshn * 365 * srokrabvetrogen * tarif - summavetrogen
					q += 'Необходимо ветрогенераторов:' + ' '
					for i in spkolvovetrogen:
						if i != 0:
							q += str(i) + ' ' + ' с мощностью ' + ' ' + str(spmoshnvetrogen[indexmoshnmikroges]) + ' ' + 'кВт;\n' 
						indexmoshnmikroges+=1
					q += 'Затраты составляют:' + ' ' + str(int(summavetrogen)) + ' ' + 'рублей, '
				else:
					q += "Вертикальные Ветрогенераторы ставить невыгодно,"
		else:
			q='Установка ветрогенераторов нерациональна в связи с условиями окружающей среды \n'
			b = 0
			spisokvozmozhnihvie[1] = 0

		e=''

		if esolnca > 0:
			pnom=1
			pinc=56#бд!!!
			snom=1.9206
			moshnsolnbat = esolnca * pnom **2 /1.2*0.2
			kolvosolbat = moshn // moshnsolnbat + 1
			summasolnbat = stoimsolnbat * kolvosolbat
			if moshn * 365 * srokrabotsolnbat * tarif > summasolnbat: 
				e += "Солнечные панели ставить выгодно, прибыль составляет: " +  str(int(moshn * 365 * srokrabotsolnbat * tarif - summasolnbat)) + ' рублей '
				estlivigodnie += 1
				c = moshn * 365 * srokrabotsolnbat * tarif - summasolnbat
				e += 'Необходимо солнечных панелей: ' +  str(int(kolvobat))  + "  "
				e += 'Затраты составляют: ' +  str(int(summasolnbat)) + ' рублей '

			else:
				e += "Солнечные панели ставить невыгодно. "
			
		else:
			e = 'Установка солнечных панелей нерациональна в связи с условиями окружающей среды. '
			c = 0
			spisokvozmozhnihvie[2] = 0

		w=''
		b=0
		a=0
		vigodi = [a,b,c]
		maxvigoda=0
		spisokvariantov = [tipmikroges, tipvetrogen, '']
		if spisokvozmozhnihvie[0] != 0:
			maxvigoda = a
		d = 0
		for i in vigodi:
			if i > maxvigoda and spisokvozmozhnihvie[d] != 0:
				maxvigoda = vigodi[d]
			d += 1
		indexs=0
		spisok = [' МиниГЭС ', ' Ветрогенераторы ', ' Солнечные панели ']
		if estlivigodnie > 0:
			d = 0
			for i in vigodi:
				if maxvigoda == i:
					indexs = d
				d += 1
			w += str(spisokvariantov[indexs]) + str(spisok[indexs]) + ' наиболее выгодны и выгода составляет: ' +  str(int(vigodi[indexs] / 15)) + 'рублей в год'
			w += ""
		else:
			for i in vigodi:
				if maxvigoda == i:
					indexs = d
				d += 1
			w+='ВИЭ не выгодны в данных условиях. '

		resp.write(s)
		resp.write(q)
		resp.write(e)
		#resp.write(w)
		#resp.write(bd)
		#qwe=0
		#qwe=min(summamikroges,summavetrogen,summasolnbat)
		#if qwe==summamikroges:
		#	resp.write(s)
		#elif qwe==summavetrogen: 
		#	resp.write(q)
		#else: 
		#	resp.write(e)	
			
			
		       

		
		return resp

	resp = HttpResponse()
	resp.status_code = 204
	resp.write('We need a request')
	return resp

def form(request):
	return render_to_response('boot.html',{})