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

import math
srokdeistvia = 15
stoimcontroller = 9779
stoimbatarei = 26300
stoiminvertorout = 9613
stoiminvertorin = 7800
stoimvetrogen = 99157
stoimsolnbat = 22014
estlivigodnie = 0
stoimakkumul = 37900
emkostakkumul = 250
spisokvozmozhnihvie = [1, 1, 1]


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
		spisokregionov = ['Саратовская область','Ульяновская область','Московская область','Ростовская область']
		region = nomerregion
		vreki = 0
		vvetra = 0
		spvreki = [2.4, 3.1, 2.2, 3.3]	
		spvvetra = [4, 5, 6, 4.2]
		spesolnca = [1100,950,1010,1290]
		sptarif = [3.43, 3.68, 3.83, 5.38]
		moshn = float(request.GET.get('moshn'))
		ppot=moshn*0.2
		moshn=moshn+ppot
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
				stoimplot=10000
				tipmikroges = ' Плотинные '
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
				summamikroges = stoimost[0] * kolvomikroges[0] + stoimost[1] * kolvomikroges[1] + stoimost[2] * kolvomikroges[2] + stoimcontroller + stoiminvertorout + stoiminvertorin + stoimakkumul
				if moshn * 365 * 24 * srokdeistvia * tarif > summamikroges: 
					s+=" Плотинные МиниГЭС ставить выгодно, прибыль составляет: "
					s+=str(int(moshn * 365 * 24 * srokdeistvia * tarif - summamikroges))
					s+='рублей'
					estlivigodnie += 1
				else:
					s="Плотинные МиниГЭС ставить невыгодно, убыток составляет: " + str(int(moshn * 365 * 24 * srokdeistvia * tarif - summamikroges)) + 'рублей'
				indexmoshnmikroges=0
				s+='Необходимо:'
				for i in kolvomikroges:
					if i != 0:
						s+='МиниГЭС с мощностью ' + str(moshnmikroges[indexmoshnmikroges]) + ' кВтч '
					indexmoshnmikroges+=1
				s+='Стоимость постройки составляет ' + str(summamikroges) + 'рублей '
				a = moshn * 365 * 24 * srokdeistvia * tarif - summamikroges
			else:
				tipmikroges = 'Деривационные '
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
				summamikroges = stoimost[0] * kolvomikroges[0] + stoimost[1] * kolvomikroges[1] + stoimost[2] * kolvomikroges[2] + stoimcontroller + stoimakkumul* math.ceil(moshn * 1000 / 0.8 / emkostakkumul * 2) + stoiminvertorout + stoiminvertorin
				if moshn * 365 * 24 * srokdeistvia * tarif > summamikroges: 
					s="Деривационные МиниГЭС ставить выгодно, прибыль составляет: " + str(int(moshn * 365 * 24 * srokdeistvia * tarif - summamikroges)) +' ' + 'рублей. '
					estlivigodnie = estlivigodnie + 1
				else:
					s="Деривационные МиниГЭС ставить невыгодно, убыток составляет: " + str(int(moshn * 365 * 24 * srokdeistvia * tarif - summamikroges)) + ' ' + 'рублей. '
				indexmoshnmikroges=0
				s += 'Необходимо: '
				for i in kolvomikroges:
					if i != 0:
						s += str(i) + ' ' + 'МиниГЭС с мощностью ' + ' ' + str(moshnmikroges[indexmoshnmikroges]) + ' ' + 'кВтч; ' 
					indexmoshnmikroges+=1
				s+='Стоимость постройки составляет: ' + ' ' + str(summamikroges) + ' ' + 'рублей '
				a = moshn * 365 * 24 * srokdeistvia * tarif - summamikroges
		else:
			s='Постройка МиниГЭС нерациональна в связи с условиями окружающей среды '
			a = 0
			spisokvozmozhnihvie[0] = 0
		q=''

		if vvetra > 0.7:
			e=0.45
			nmax=0
			maxdnvetr=0
			r=1
			spdnvetra=[[0,0,0,1,5,6,3,2,1,3,6,7,5,6,5,3,6,8,9,6,3,1,4,5,5,4,2,1,7,2],[1,2,3,4,5,6,3,2,1,3,6,7,5,6,5,3,6,8,9,6,3,1,4,5,5,4,2,1,7,2],[1,2,3,4,5,6,3,2,1,3,6,7,5,6,5,3,6,8,9,6,3,1,4,5,5,4,2,1,7,2],[1,2,3,4,5,6,3,2,1,3,6,7,5,6,5,3,6,8,9,6,3,1,4,5,5,4,2,1,7,2]]
			for i in spdnvetra[0]:
				if i<=1:
					maxdnvetr+=1
				else:
					if maxdnvetr>nmax:
						nmax=maxdnvetr
					maxdnvetr=0	

			if vvetra > 3:
				tipvetrogen = 'Горизонтальные '
				moshnvetrogen = e*vvetra**3*1.29*3.14*r**2/2
				kolvovetrogen = moshn // moshnvetrogen + 1
				summavetrogen = stoimvetrogen * kolvovetrogen + stoimcontroller + stoiminvertorout + nmax*stoimakkumul * math.ceil(moshn * 1000 / 0.8 / emkostakkumul * 2) + stoiminvertorin
				if moshn * 365 * 24 * srokdeistvia * tarif > summavetrogen: 
					q += "Горизонтальные Ветрогенераторы ставить выгодно, прибыль составляет: " + str(int(moshn * 365 * 24 * srokdeistvia * tarif - summavetrogen)) + ' ' + 'рублей'
					estlivigodnie += 1
				else:
					q += "Горизонтальные Ветрогенераторы ставить невыгодно, убыток составляет: "+  str(int(moshn * 365 * 24 * srokdeistvia * tarif - summavetrogen)) + ' ' + 'рублей'
				b = moshn * 365 * 24 * srokdeistvia * tarif - summavetrogen
				q+='. Необходимо ветрогенераторов:' + ' ' +  str(int(kolvovetrogen))
				q += '. Стоимость постройки составляет: ' + str(int(summavetrogen)) + ' ' + 'рублей '
			else:
				tipvetrogen = 'Вертикальные'
				moshnvetrogen = e*vvetra**3*1.29*3.14*r**2/2
				kolvovetrogen = moshn // moshnvetrogen + 1
				summavetrogen = stoimvetrogen * kolvovetrogen + stoimbatarei + stoimcontroller + stoiminvertorout + stoimakkumul * math.ceil(moshn * 1000 / 0.8 / emkostakkumul * 2) + stoiminvertorin
				if moshn * 365 * 24 * srokdeistvia * tarif > summavetrogen: 
					q += "Вертикальные Ветрогенераторы ставить выгодно, прибыль составляет: " +  str(int(moshn * 365 * 24 * srokdeistvia * tarif - summavetrogen)) + ' ' + 'рублей'
					estlivigodnie += 1
				else:
					q += "Вертикальные Ветрогенераторы ставить невыгодно, убыток составляет: " +  str(int(moshn * 365 * 24 * srokdeistvia * tarif - summavetrogen)) + ' ' + 'рублей'
				b = moshn * 365 * 24 * srokdeistvia * tarif - summavetrogen
				q += 'Необходимо ветрогенераторов:' + ' ' + str(int(kolvovetrogen))
				q += 'Стоимость постройки составляет:' + ' ' + str(int(summavetrogen)) + ' ' + 'рублей '
		else:
			q='Установка ветрогенераторов нерациональна в связи с условиями окружающей среды '
			b = 0
			spisokvozmozhnihvie[1] = 0

		e=''

		if esolnca > 1050:
			pnom=0.3
			pinc=3
			moshnsolnbat = esolnca * pnom * 0.85 / pinc
			kolvosolbat = moshn // moshnsolnbat + 1
			summasolnbat = stoimsolnbat * kolvosolbat + stoimcontroller + stoiminvertorout + stoimakkumul * math.ceil(moshn * 1000 / 0.8 / emkostakkumul * 2)*2 + stoiminvertorin
			if moshn * 365 * 24 * srokdeistvia * tarif > summasolnbat: 
				e += "Солнечные панели ставить выгодно, прибыль составляет: " +  str(int(moshn * 365 * 24 * srokdeistvia * tarif - summasolnbat)) + ' рублей '
				estlivigodnie += 1
			else:
				e += "Солнечные панели ставить невыгодно, убыток составляет: " + str(int(moshn * 365 * 24 * srokdeistvia * tarif - summasolnbat)) + ' рублей'
			c = moshn * 365 * 24 * srokdeistvia * tarif - summasolnbat
			e += '. Необходимо солнечных панелей: ' +  str(int(kolvosolbat))
			e += '. Стоимость постройки составляет: ' +  str(int(summasolnbat)) + ' рублей '
		else:
			e = 'Установка солнечных панелей нерациональна в связи с условиями окружающей среды '
			c = 0
			spisokvozmozhnihvie[2] = 0

		w=''

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
			w+='ВИЭ не выгодны в данных условиях и минимальный убыток при установке ' + str(spisok[indexs]) + ' составляет ' + str(int(vigodi[indexs] / 15)) + 'рублей в год'

		#resp.write(s)
		#resp.write(q)
		#resp.write(e)
		#resp.write(w)
		qwe=0
		qwe=min(summamikroges,summavetrogen,summasolnbat)
		if qwe==summamikroges:
			resp.write(s)
		elif qwe==summavetrogen: 
			resp.write(q)
		else: 
			resp.write(e)	
			
			
		       

		
		return resp

	resp = HttpResponse()
	resp.status_code = 204
	resp.write('We need a request')
	return resp

def form(request):
	return render_to_response('boot.html',{})

	https://maps.googleapis.com/maps/api/place/textsearch/json?query=natural_feature&radius=6000&language=ru&opennow&location="+x+","+y+"&key=AIzaSyDMkPyS3cWd1qIDDXYQHSLJ4PrV6ILkgVw"